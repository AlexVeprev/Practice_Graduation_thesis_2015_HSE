# -*- coding: utf-8 -*-
import geo_tags
import people_detection
import tracer as trace
import os
import subprocess


@trace.enter
def write_tags_to_image_via_et(image, tags):
    from main_config import exiftool

    options = ['-codedcharacterset=UTF8',
               '-charset', 'iptc=cp1251',
               '-charset', 'filename=cp1251',
               '{0}'.format(image)]

    for tag in tags:
        if tag.lower() == "keywords":
            for i in tags[tag]:
                options.append('-iptc:{0}={1}'.format(tag, i))
        else:
            options.append('-iptc:{0}={1}'.format(tag, tags[tag]))

    cmd = [exiftool]
    cmd.extend(options)

    trace.debug('Cmd: {0}'.format(cmd))

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    trace.debug('stdout: {0}; stderr: {1}'.format(out, err))

    if p.returncode:
        trace.error('Unexpected return code: {0}; cmd: {1}'.format(p.returncode, cmd))

    return p.returncode


@trace.enter
def get_tags(image):
    tags = geo_tags.get_geo_tags_in_et_format(image)
    if 'keywords' in tags.keys():
        tags['keywords'].extend(people_detection.get_keywords(image))
    else:
        tags['keywords'] = people_detection.get_keywords(image)

    return tags

'''
path = "D:/_test/control_set_01"
import exiftool

for image in os.listdir(path):
    get_tags(os.path.join(path, image))
'''