# -*- coding: utf-8 -*-
# 0002_profile_data_migration
# Data migration for user profile association with existing users.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Jan 28 08:40:19 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: 0002_profile_data_migration.py [] benjamin@bengfort.com $

"""
Data migration for user profile association with existing users.
Generated by Django 1.9.1 on 2016-01-28 13:37
"""

##########################################################################
## Imports
##########################################################################

from __future__ import unicode_literals

import hashlib

from django.db import migrations
from django.contrib.auth.models import User

##########################################################################
## Create User Profiles for Existing Users
##########################################################################

def update_users_profile(apps, schema_editor):
    """
    We can't import the User model directly as it may be a newer version
    than this migration expects. We use the historical version.

    https://docs.djangoproject.com/en/1.9/topics/migrations/
    """
    Profile = apps.get_model('members', 'Profile')
    User = apps.get_model('auth', 'User')

    # Loop through all existing users and assign their profile
    for user in User.objects.all():
        digest = hashlib.md5(user.email.lower()).hexdigest()
        Profile.objects.create(user=user, email_hash=digest)


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.RunPython(update_users_profile),
    ]
