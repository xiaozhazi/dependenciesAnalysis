'''
Module that provides basic functions to analysis dependency
accross one or more pom.xml files.
'''

import collections
from xml.etree import ElementTree
import sys

POM_NS = 'http://maven.apache.org/POM/4.0.0'
COORDS = ['groupId', 'artifactId', 'version']

def _get_tag(name):
    '''Helper functions to construct tag names with the pom URI.'''
    return '{%s}%s' % (POM_NS, name)

Artifact = collections.namedtuple('Artifact', COORDS)

def __get_artifact_from_node(node):
    '''Attempt to extract artifact coordinates from a node.'''
    coordinates = {}
    for tag in COORDS:
        child = node.find(_get_tag(tag))
        coordinates[tag] = None if child is None else child.text
    if coordinates['artifactId'] is not None:
        return Artifact(**coordinates)
    else:
        return None

def __get_parent(root):
    '''Attempt to find a parent artifact.'''
    parent = root.find(_get_tag('parent'))
    if parent is not None:
        return __get_artifact_from_node(parent)
    else:
        return None

def __get_dependencies(root):
    '''Find all artifact dependencies.'''
    dependencies = root.find(_get_tag('dependencies'))
    if dependencies is not None:
        return [__get_artifact_from_node(d) for d in dependencies]
    else:
        return list()

def parse(filename):
    with open(filename) as f:
        tree = ElementTree.parse(f)
    results = {}
    results['artifact'] = __get_artifact_from_node(tree)
    parent = __get_parent(tree)
    results['dependencies'] = __get_dependencies(tree)
    return results

if __name__ == '__main__':
    print parse(sys.argv[1])
