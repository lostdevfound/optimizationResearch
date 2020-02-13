
import geopy.distance

def kmDist(locA, locB):
    """ Measrue geodesic distance in kilometers between to Location objects."""
    set1 = locA.get_pos()
    set2 = locB.get_pos()
    return geopy.distance.distance(set1,set2).km


def isClose(locA, locB, km = 1):
    """ Check if two Location objects are within a distance """
    check = True if kmDist(locA, locB) <= km else False
    return check


class Location:
    """ Super class of Location """
    def __init__(self, lat, long, id, neighbors):
        self.lat = lat
        self.long = long
        self.id = id
        self.neighborhood = neighbors

    def get_pos(self):
        """ get lat long tupel of the location """
        return (self.lat, self.long)


    def findNeighbors(self, neighborList, km):
        """ Find Locations within km radius """
        self.neighborhood = []

        for neighbor in neighborList:

            if isClose(self, neighbor, km):
                self.neighborhood.append(neighbor)

        return self.neighborhood



class BusStop(Location):
    """ Bus stop class"""
    def __init__(self, lat, long, id, blocks, j, connectedness=0):
        super().__init__(lat, long, id, blocks)
        self.demand = 0
        self.weight = 1
        self.connectedness = connectedness
        self.competitors = 0
        self.j = j  # this is an index which is used in optimization formula

    def __repr__(self):
        return f'busStop id:{self.id}'


    def distTo(demandNode):
        pass


    def findCompetitors(self, busStopList, radius):
        """ Find competitors (other bus stops) which are within radius """

        self.competitors = []

        for stop in busStopList:
            # if other stops within the radius and other stop is not the stop we measure from then add
            if kmDist(self,stop) <= radius and self is not stop:
                self.competitors.append(stop)

        return self.competitors


    def normalization(self, alpha, beta, demandNode):
        if self.competitors == 0:
            raise Exception('First need to find bus stop competitors by calling findCompetitors.')

        # if no competitors the normalization is 1
        if len(self.competitors) == 0:
            return 1

        res = 0

        for compet in self.competitors:
            res += compet.weight**alpha*kmDist(compet,demandNode)**(-beta)

        return res
        # add self to nomalization
        # return res + self.weight**alpha*kmDist(self,demandNode)**(-beta)


class Block(Location):
    """ Demand point, can be Dissemintaion Area or Dissemintaion Block """
    def __init__(self, lat, long, id, pop, dwel, stops):
        super().__init__(lat, long, id, stops)
        self.pop = pop
        self.dwel = dwel
        self.demand = 0
    def __repr__(self):
        return f'block id:{self.id}'



if __name__ == '__main__':
    stop1 = BusStop(52,10,101,[])
    stop2 = BusStop(52.01,10.1,102,[])
    stops = [stop1, stop2]

    block1 = Block(52.0002,10.0002,101, 10, 10,[])
    block2 = Block(52.0003,10.0003,102, 10, 10,[])
    blocks = [block1, block2]

    stop1.findNeighbors(blocks)
    print(stop1.neighborhood)

    block1.findNeighbors(stops)
    print(block1.neighborhood)
