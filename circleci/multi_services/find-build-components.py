#!/usr/bin/env python3

import yaml
import fileinput
import sys
import argparse

BUILD_COMPONENTS = '.circleci/build-components.yaml'

def find_component(components, file_path):
    found_components = []
    for component, component_paths in iter(components.items()):
        hit_count = 0
        for component_path in component_paths:
            if component_path.find('(not)') != -1:
                ncomponent_path = component_path.replace('(not)','')
                if file_path.startswith(ncomponent_path):
                    hit_count -= 1
            elif file_path.startswith(component_path):
                hit_count += 1
        if hit_count > 0:
            found_components.append(component)
    return set(found_components)


def main():
    """
    Script accepts either:
        a) list of changed files line-by-line on stdin, e.g.
           output of `git diff --name-only` (preferred);
        b) name of a file containing list of files to analyze.

    Script outputs a comma-separated list of components to build.

    Build components are defined in .circleci/build-components.yaml.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_components', type=str, default=BUILD_COMPONENTS,
                        help='File with build components and their dependencies')
    parser.add_argument('files', metavar='FILE', nargs='*',
                        help='files to read, if empty, stdin is used')
    args = parser.parse_args()

    with open(args.build_components, 'r') as components_file:
        build_components = yaml.safe_load(components_file)

    found_components = []
    for line in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
        found_components += find_component(build_components, line)

    print(",".join(set(found_components)))
    return 0

if __name__ == '__main__':
    sys.exit(main())
