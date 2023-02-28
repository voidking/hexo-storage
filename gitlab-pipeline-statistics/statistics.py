#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import datetime

# GitLab API访问令牌
TOKEN = 'xxx'

# GitLab API基础URL
API_BASE_URL = 'https://gitlab.voidking.com/api/v4'

# 获取所有项目的API URL
GET_PROJECTS_URL = API_BASE_URL + '/projects'

# 获取项目的pipeline列表的API URL
GET_PIPELINES_URL = API_BASE_URL + '/projects/{project_id}/pipelines'

# 获取pipeline中job的运行时间的API URL
GET_JOB_URL = API_BASE_URL + '/projects/{project_id}/pipelines/{pipeline_id}/jobs'

# 请求头
headers = {'Authorization': 'Bearer ' + TOKEN}

# 统计所有pipeline的总耗时
total_duration = 0

# 统计pipeline的次数
total_times = 0
total_success_times = 0
total_failed_times = 0
total_canceled_times = 0
total_skipped_times = 0
more_than_300_times = 0
more_than_600_times = 0
more_than_1800_times = 0
more_than_3600_times = 0

# 获取当前时间和两个月前的时间
now = datetime.datetime.utcnow()
two_months_ago = now - datetime.timedelta(days=60)

# 获取所有项目的列表
projects = []
page = 1
while True:
    params = {'page': page}
    resp = requests.get(GET_PROJECTS_URL, headers=headers, params=params)
    if not resp.ok:
        print('Failed to get projects:', resp.content)
        break
    projects.extend(resp.json())
    if not resp.links.get('next'):
        break
    page += 1

print(len(projects))

# 遍历每个项目，并获取它们的pipeline列表
for project in projects:
    project_id = project['id']
    project_name = project['name']
    print('Project:', project_name)

    # 获取该项目的所有pipeline列表
    # resp = requests.get(GET_PIPELINES_URL.format(project_id=project_id), headers=headers, params={'status': 'success'})
    # if not resp.ok:
    #     print('Failed to get pipelines:', resp.content)
    #     continue

    # 获取该项目最近两个月内更新过的pipeline列表
    updated_after = two_months_ago.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    updated_before = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    resp = requests.get(GET_PIPELINES_URL.format(project_id=project_id),
                        headers=headers,
                        params={'updated_after': updated_after, 'updated_before': updated_before})
    if not resp.ok:
        print('Failed to get pipelines:', resp.content)
        continue

    # 遍历该项目的每个pipeline，并统计它们的耗时
    pipelines = resp.json()
    for pipeline in pipelines:
        # print(pipeline)
        pipeline_id = pipeline['id']
        pipeline_duration = 0

        # 获取该pipeline中每个job的运行时间，并累加到pipeline_duration中
        resp = requests.get(GET_JOB_URL.format(project_id=project_id, pipeline_id=pipeline_id), headers=headers)
        if not resp.ok:
            print('Failed to get jobs:', resp.content)
            continue
        jobs = resp.json()
        for job in jobs:
            job_duration = job.get('duration', 0)
            if job_duration:
                pipeline_duration += job_duration

        # 输出该pipeline的耗时
        # pipeline_name = pipeline['name']
        pipeline_id = pipeline['id']
        pipeline_created_at = pipeline['created_at']
        # pipeline_finished_at = pipeline['finished_at']
        pipeline_finished_at = pipeline['updated_at']
        pipeline_status = pipeline['status']
        print('Pipeline: {}, Created At: {}, Finished At: {}, Duration: {}s, Status: {}'.format(
            pipeline_id,
            pipeline_created_at,
            pipeline_finished_at,
            pipeline_duration,
            pipeline_status))

        # 累加该pipeline的耗时到总耗时中
        # total_duration += pipeline_duration

        # 统计pipeline的次数
        total_times = total_times + 1
        if pipeline_duration > 300:
            more_than_300_times += 1
        if pipeline_duration > 600:
            more_than_600_times += 1
        if pipeline_duration > 1800:
            more_than_1800_times += 1
        if pipeline_duration > 3600:
            more_than_3600_times += 1
        if pipeline_status == 'success':
            total_success_times += 1
        if pipeline_status == 'failed':
            total_failed_times += 1
        if pipeline_status == 'canceled':
            total_canceled_times += 1
        if pipeline_status == 'skipped':
            total_skipped_times += 1


# 输出所有pipeline的总耗时
# print('Total duration: {}s'.format(total_duration))
# 输出统计结果
print('Total times: {}'.format(total_times))
print('Total success times: {}'.format(total_success_times))
print('Total failed times: {}'.format(total_failed_times))
print('Total canceled times: {}'.format(total_canceled_times))
print('Total skipped times: {}'.format(total_skipped_times))
print('More than 300 seconds times: {}'.format(more_than_300_times))
print('More than 600 seconds times: {}'.format(more_than_600_times))
print('More than 1800 seconds times: {}'.format(more_than_1800_times))
print('More than 3600 seconds times: {}'.format(more_than_3600_times))
print('Failure rates: {}'.format(1.0*total_failed_times/total_times))


