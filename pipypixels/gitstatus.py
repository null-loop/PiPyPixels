from datetime import datetime

from PIL import Image, ImageDraw
from ghapi.core import GhApi

from pipypixels.graphics import assets
from pipypixels.graphics.shared import Matrix
from pipypixels.screens import ImageScreen


class GitStatusConfiguration:
    pat = "",
    repos = []

    @staticmethod
    def create_from_json(screen_json_config):
        config = GitStatusConfiguration()
        config.pat = screen_json_config["pat"]
        config.repos = GitRepoConfiguration.create_many_from_json_config(screen_json_config)
        return config

class GitRepoConfiguration:
    name = ""
    display = ""
    checks = []

    @staticmethod
    def create_many_from_json_config(screen_json_config):
        repos = []
        for repo_json in screen_json_config["repos"]:
            repo = GitRepoConfiguration()
            repo.name = repo_json["name"]
            repo.display = repo_json["display"]
            repo.checks = repo_json["checks"]
            repos.append(repo)
        return repos

class GitStatus:
    label = ""
    state = list()
    pr_count = 0
    branch_count = 0

class GitStatusScreen(ImageScreen):
    def __init__(self, config: GitStatusConfiguration, matrix: Matrix):
        super().__init__(60, matrix)
        self.__config = config
        self.__small_font = assets.font_custom(12)
        self.__big_font = assets.font_custom(23)
        self.__check_names_to_id_map = {}
        self.__all_runs = {}

    def _render_image(self) ->Image:
        output_image = Image.new('RGB',(self._matrix.config.overall_led_width, self._matrix.config.overall_led_height))
        output_image_draw = ImageDraw.Draw(output_image)

        row = 0
        for repo in self.__config.repos:
            status = self.__get_repo_status(repo)
            self.__render_repo_status(status, row, output_image_draw)
            row = row + 1

        return output_image

    def __render_repo_status(self, info: GitStatus, row, draw):

        row_height = 23
        y_offset = (row * row_height) + 1 + (row * 2)
        overall_status = 'success'

        if len(info.state) > 0:
            current_x = 74

            status_height = 4
            if len(info.state) == 1: status_height = 16
            if len(info.state) == 2: status_height = 8
            if len(info.state) == 3: status_height = 4
            if len(info.state) == 4: status_height = 3

            current_y = y_offset + row_height - 3

            for builds in info.state:
                # look at the latest build for the overall_status
                latest_build = builds[0]
                if latest_build == 'pending': overall_status = 'pending'
                if latest_build == 'failure' or latest_build == 'startup_failure': overall_status = 'failure'
                if latest_build == 'cancelled': overall_status = 'cancelled'
                states = builds.copy()
                states.reverse()
                for state in states:
                    run_color = 'DarkBlue'
                    if state == 'success': run_color = 'DarkGreen'
                    if state == 'failure' or state == 'startup_failure': run_color = 'DarkRed'
                    if state == 'cancelled': run_color = 'DarkGrey'
                    draw.rectangle([current_x, current_y - status_height, current_x + 2, current_y], fill=run_color)
                    current_x = current_x + 3
                current_y = current_y - status_height - 1
                current_x = 74

            current_y = y_offset + row_height - 3
            draw.line([74, current_y - 17, 94, current_y - 17], fill='DimGrey')
            draw.line([74, current_y + 1, 94, current_y + 1], fill='DimGrey')

        summary_color = 'DarkBlue'
        if overall_status == 'success': summary_color = 'DarkGreen'
        if overall_status == 'failure' or overall_status == 'startup_failure': summary_color = 'DarkRed'

        draw.line([2, y_offset + row_height + 1, 125, y_offset + row_height + 1], fill='DimGrey')
        draw.text([2, y_offset - 2], info.label, font=self.__big_font, fill=summary_color)

        draw.bitmap([98, y_offset], assets.git_pull_request, fill='DimGrey')
        draw.bitmap([98, y_offset + 12], assets.git_branch, fill='DimGrey')

        draw.text([112, y_offset - 2], "{0}".format(info.pr_count), font=self.__small_font, fill='DimGrey')
        draw.text([112, y_offset + 10], "{0}".format(info.branch_count), font=self.__small_font, fill='DimGrey')

    def __get_repo_status(self, config: GitRepoConfiguration) -> GitStatus:
        api = GhApi(owner="PureGymGroup", repo=config.name, token=self.__config.pat)

        state = []
        for check in config.checks:
            if check not in self.__check_names_to_id_map:
                if check not in self.__all_runs:
                    self.__all_runs[config.name] = api.actions.list_workflow_runs_for_repo(owner="PureGymGroup", repo=config.name, branch="main", per_page=100)
                for run in self.__all_runs[config.name].workflow_runs:
                    if run.name == check:
                        self.__check_names_to_id_map[check] = run.workflow_id
            workflow_id = self.__check_names_to_id_map[check]
            workflow_runs = api.actions.list_workflow_runs(owner="PureGymGroup", repo=config.name, branch="main", workflow_id=workflow_id, per_page=100)
            # get only the last run on each of the last 7 days
            check_states = []
            day = 0
            last_date = ""
            for run in workflow_runs.workflow_runs:
                if day > 6:
                    break
                date = datetime.strptime(run.updated_at,'%Y-%m-%dT%H:%M:%SZ')
                if date.date() != last_date:
                    last_date = date.date()
                    check_states.append(run.conclusion)
                    day = day + 1
            state.append(check_states)

        status = GitStatus()
        status.label = config.display
        status.pr_count = len(api.pulls.list(owner="PureGymGroup", repo=config.name))
        status.branch_count = len(api.repos.list_branches(owner="PureGymGroup", repo=config.name))
        status.state = state
        return status