# -*- coding: utf-8 -*-

from atx_te_watcher.te import TePageCrawler

crawler = TePageCrawler()
crawler.start()

digest = crawler.get_contents_digest()
print('current timetable digest is ', digest)

print('--------------------------------------------')

schedule_list = crawler.get_timetable()
for schedule in schedule_list:
    print(schedule.date.strftime('%Y/%m/%d %H:%M:%S'), schedule.story_title)

print('--------------------------------------------')

new_story_title, new_story_body = crawler.get_newest_story()
print(new_story_title)
print('---------------------')
print(new_story_body)

print('--------------------------------------------')

