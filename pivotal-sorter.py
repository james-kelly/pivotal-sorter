from functools import cmp_to_key

import click
import requests


def compare(a, b):
    print("1: ", a['name'])
    print("2: ", b['name'])

    if input("Which is higher priority? [1|2]") == "1":
        return 1
    else:
        return -1


@click.command()
@click.option('--token', help='PivotalTracker API Token.')
@click.option('--project-id', help='PivotalTracker project id.')
@click.option('--icebox', default=False, is_flag=True, help='Organize icebox items.')
def pivotal_sorter(token, project_id, icebox):
    if icebox:
        group = with_state = 'unscheduled'
    else:
        with_state = 'unstarted'
        group = 'scheduled'

    stories = requests.get(
        "https://www.pivotaltracker.com/services/v5/projects/{project_id}/stories".format(project_id=project_id),
        headers={u'X-TrackerToken': token}, params={'with_state': with_state}).json()

    stories = sorted(stories, key=cmp_to_key(compare), reverse=True)

    for i, story in enumerate(stories):
        if i == 0:
            before_id = stories[i + 1]['id']
            after_id = None
        elif i == len(stories) - 1:
            before_id = None
            after_id = stories[i - 1]['id']
        else:
            before_id = stories[i + 1]['id']
            after_id = stories[i - 1]['id']

        response = requests.put(
            "https://www.pivotaltracker.com/services/v5/projects/{project_id}/stories/{story_id}".format(
                project_id=project_id,
                story_id=story['id']), headers={u'X-TrackerToken': token},
            data={"before_id": before_id, "after_id": after_id, 'group': group})

        print(response.json(), before_id, after_id, story['name'])


if __name__ == "__main__":
    pivotal_sorter()
