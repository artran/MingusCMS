import os

from django.conf import settings
from django.core.management.base import NoArgsCommand

from git import Repo


class Command(NoArgsCommand):
    help = 'Create the git repositories that Mingus uses to store the CMS content.'

    def handle_noargs(self, **options):
        if os.path.exists(settings.REPO_ROOT):
            print('Repositories already exist, not recreating them.')
        else:
            print('Creating repositories at %s.' % settings.REPO_ROOT)
            live_repo = Repo.init(settings.REPO_ROOT + '/live_content')
            preview_repo = Repo.init(settings.REPO_ROOT + '/preview_content')

            for repo in (live_repo, preview_repo):
                for directory in ('cms_images', 'cms_media', 'cms_templates'):
                    os.mkdir(os.path.join(repo.working_tree_dir, directory))
