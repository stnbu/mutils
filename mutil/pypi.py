# -*- coding: utf-8 -*-


def meta_setup(package, kwargs={}):
    _author = 'Mike Burr'
    _email = 'mburr@unintuitive.com'
    __author__ = '%s <%s>' % (_author, _email)

    from distutils.core import setup
    import time

    # README.rst dynamically generated:
    with open('README.md', 'w') as f:
        f.write(package.__doc__)

    name = package.__name__

    def read(file):
        with open(file, 'r') as f:
            return f.read().strip()

    setup_kwargs = dict(
        name=name,
        version='0.0.1-%s' % time.time(),
        long_description=read('README.md'),
        author=_author,
        author_email=_email,
        provides=[name],
        packages=[name],
    )

    setup_kwargs.update(kwargs)

    setup(**setup_kwargs)
