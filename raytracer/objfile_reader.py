import math
import raytracer as rt


class GroupInfo:
    __slots__ = ['name', 'group']

    def __init__(self, name, group):
        self.name = name
        self.group = group


class Parser:
    __slots__ = ['vertices', 'groupinfos', 'normals']

    def __init__(self):
        self.vertices = [None]
        self.groupinfos = []
        self.normals = [None]

    @property
    def numvertices(self):
        return len(self.vertices) - 1

    @property
    def numnormals(self):
        return len(self.normals) - 1

    def parse_obj_file(self, filename, autoscale=True):
        self.vertices = [None]
        self.groupinfos = []
        self.normals = [None]

        minx = miny = minz = math.inf
        maxx = maxy = maxz = -math.inf
        sx = sy = sz = scale = 0

        if autoscale:
            f = open(filename, 'r')
            line = f.readline()
            while line:
                linesplit = line.split()
                if len(linesplit) > 0:
                    if linesplit[0] == 'v':
                        assert len(linesplit) >= 4
                        x = float(linesplit[1])
                        y = float(linesplit[2])
                        z = float(linesplit[3])
                        if x < minx:
                            minx = x
                        if x > maxx:
                            maxx = x
                        if y < miny:
                            miny = y
                        if y > maxy:
                            maxy = y
                        if z < minz:
                            minz = z
                        if z > maxz:
                            maxz = z

                line = f.readline()
            f.close()

            if math.isinf(minx):
                # there were no vertices in the file, just exit
                return

            print('Boundaries - ({}, {}, {}) to ({}, {}, {})'.format(minx, miny, minz, maxx, maxy, maxz))
            sx = maxx-minx
            sy = maxy-miny
            sz = maxz-minz
            scale = max(sx, sy, sz) / 2
            print('Scale - {}'.format(scale))

        f = open(filename, 'r')
        current_groupname = ''
        line = f.readline()

        while line:
            linesplit = line.split()
            if len(linesplit) > 0:
                # TODO - technically objects ('o') can be made up of groups ('g').
                # however, we will treat objects and groups as synonyms for right now.
                if linesplit[0] in ('g', 'o'):
                    assert len(linesplit) >= 2
                    # group name
                    current_groupname = linesplit[1]
                else:
                    current_group = self.get_group_by_name(current_groupname)
                    if current_group is None:
                        current_group = rt.ObjectGroup()
                        self.groupinfos.append(GroupInfo(current_groupname, current_group))
                    if linesplit[0] == 'v':
                        # vertex
                        assert len(linesplit) >= 4
                        x = float(linesplit[1])
                        y = float(linesplit[2])
                        z = float(linesplit[3])

                        if autoscale:
                            # scale it - see https://forum.raytracerchallenge.com/thread/27/triangle-mesh-normalization
                            x = (x - (minx + sx/2)) / scale
                            y = (y - (miny + sy/2)) / scale
                            z = (z - (minz + sz/2)) / scale

                        self.vertices.append(rt.Point(x, y, z))
                    elif linesplit[0] == 'f':
                        # face (a.k.a. polygons)
                        assert len(linesplit) >= 4
                        lsints = []
                        normints = []
                        i = 1
                        while i < len(linesplit):
                            vertexinfo = linesplit[i].split('/')
                            if not vertexinfo[0].isdigit():
                                break
                            lsints.append(int(vertexinfo[0]))
                            if len(vertexinfo) >= 2:
                                normints.append(int(vertexinfo[2]))
                            i += 1
                        assert len(lsints) >= 3
                        assert len(normints) == 0 or len(normints) == len(lsints)
                        i = 2
                        while i < len(lsints):
                            if len(normints) == 0:
                                t = rt.Triangle(self.vertices[lsints[0]], self.vertices[lsints[i-1]],
                                                self.vertices[lsints[i]])
                            else:
                                t = rt.SmoothTriangle(self.vertices[lsints[0]], self.vertices[lsints[i-1]],
                                                      self.vertices[lsints[i]], self.normals[normints[0]],
                                                      self.normals[normints[i-1]], self.normals[normints[i]])
                            i += 1
                            current_group.addchild(t)
                    elif linesplit[0] == 'vn':
                        # vertex normals
                        assert len(linesplit) >= 4
                        self.normals.append(rt.Vector(float(linesplit[1]), float(linesplit[2]), float(linesplit[3])))
            line = f.readline()
        f.close()

    def get_group_by_name(self, name=''):
        for i in self.groupinfos:
            if i.name == name:
                return i.group

        return None

    def obj_to_group(self):
        g = rt.ObjectGroup()
        for groupinfo in self.groupinfos:
            g.addchild(groupinfo.group)
        return g
