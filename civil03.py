import collections 
import matplotlib.pyplot as plt

point = collections.namedtuple('Point', " sta elev ")
pi    = collections.namedtuple('Point_of_Intersection', " sta elev Length") 
pog   = collections.namedtuple('Point_on_grade', " sta elev grade") 
seg =   collections.namedtuple('ProG_segment',"sta_1 elev_1 grade_1 sta_2 elev_2 grade_2 Length rate") 

class ProG:
    def __init__(self, name, pointList ):
        ''' ProG are defined with a list.  
        The list must start and end with a point type
        midpoints must be pt_of_I type'''
        self.name = name 
        self.pointList = pointList
        # when called correctly I can validate right here with
        # self.validate()   where  the function has been defined
        # def  validate(self)
        if ( self.validate()):  
            print ("Print seems good")
            print ("Point info:")
            print ( self.definion_points() )
            self.pcs=self.pc_list()
            self.segments=self.ProG_segments()

    def definion_points(self):
        for n,p in enumerate(self.pointList):
            print( f"{n}    {p}")

    def validate(self):
        ''' Return true if list start and ends with points
        and has pt_of_I for midpoints.  PC and PT must be in order'''
        pl = self.pointList

        if not isinstance( pl[0], point ):
            return False
        if not isinstance( pl[-1], point ):
            return False
        
        last = pl[0].sta
        for p in pl[1:-1]: 
            #print(type (p))
            if (not isinstance( p, pi ) or
                p.Length < 0.0 or
                p.sta - p.Length/2.0 < last ):
                return False
            last = p.sta + p.Length/2.0 
        if last > pl[-1].sta :
            return False
        # must be ok up to this point fill in the segments
        return True



    def pc_list(self):
        ''' Produces a list of point actually on the grade line.  Takes pt_on_I and 
         convets them to PC and PT.  Note, ProG is defined with start, PI's and end.'''
        pl = self.pointList
        pc_list = list()           #empty
        
        near = pl[0]
        far =  pl[1]
        tmp = pog( near.sta, near.elev, calc_grade(near,far) )
        pc_list.append(  tmp  )  #add first point

        for n, pi in enumerate(pl[1:-1]):     #loop over all PI add two points each time
            n = n+1
            near = pi
            far =  pl[n-1]
            pc_list.append( L_over_2(near, far) )

            near = pi
            far =  pl[n+1]
            pc_list.append( L_over_2(near, far) )

            
        near = pl[-1]
        far =  pl[-2]
        tmp = pog( near.sta, near.elev, calc_grade(near,far) )
        pc_list.append(  tmp  )  #add last point

        return pc_list
    
    def ProG_segments(self):
        ''' Produce a list of segment where the rate of change on the segment is constant'''
        segments = []
        pcs = self.pc_list()
        for start, end in zip( pcs[:-1],pcs[1:] ):
            Length = end.sta - start.sta
            d_grade = end.grade - start.grade
            r = 0.0
            if Length > 0:
                rate = d_grade / Length 
            new_seg = seg( start.sta , start.elev, start.grade,
                           end.sta,    end.elev,   end.grade,
                           Length,  rate ) 
            segments.append( new_seg )
        return segments

    def profile_grade(self, sta):
        seg_list = self.ProG_segments()
        low = seg_list[0].sta_1
        high = seg_list[-1].sta_2 
        if sta < low or sta > high:
            print( f"sta of {sta} not between {low} and {high}")
        for s in seg_list:
            low =  s.sta_1
            high = s.sta_2 
            if sta >= low and sta < high:
                #print (s)
                d_x = sta - low
                tmp_elev = s.elev_1 + d_x * s.grade_1 + (s.rate / 2.0 ) * d_x * d_x
                return tmp_elev
        return "error"


def cmp(a, b):
    return (a > b) - (a < b) 

def calc_grade(near, far):
    d_sta = far.sta - near.sta
    d_elev = far.elev - near.elev
    grade = 0.0
    if d_sta != 0:
        grade =  d_elev / d_sta
    return grade

def L_over_2(near, far):
    d_sta = far.sta - near.sta
    sign = cmp(d_sta, 0)
    grade =  sign * calc_grade( near, far)
    sta =   near.sta + sign * (near.Length /2.0)
    elev = near.elev + near.Length/2.0 * grade 
    return pog( sta, elev, sign*grade)


if __name__ == "__main__":
    print ("start")
    start = point( 100, 10)
    pi_1  = pi( 200, 20, 29)
    pi_2  = pi( 300,  3, 29)
    pi_3 =  pi( 400, 44, 160)
    end =   point(500, 44)
    pg_list = [ start, pi_1, pi_2, pi_3, end ] 

    pgl = ProG( name = "somegreatName", pointList = pg_list )
    #pgl.definion_points()
    print( pgl.validate() )
    if  pgl.validate():
        x = []
        y = []
        for i in pg_list:
           x.append(i.sta)
           y.append(i.elev)

        plt.style.use('seaborn-whitegrid')
        plt.plot(x, y, 'o', color='red');

        
        x3 = []
        y3 = []
        for i in range(x[0], x[-1]):
           x3.append(i)
           y3.append( pgl.profile_grade(i) )
        plt.plot(x3, y3, 'o', color='blue');
        plt.show()
        print( pgl.pcs )
        print( pgl.segments )
    
