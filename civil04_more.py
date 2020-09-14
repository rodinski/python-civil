#from collections import namedtuple
from pprint import PrettyPrinter as pp
class ProG():
    def __init__(self, name="blank_name", pi_list = [] ):
        self.name = name
        self.pi_list = pi_list
        pass

    def __repr__(self):
        tmp = f'{self.__class__.__name__} = \n'
        tmp += f'    name:{self.name}'
        tmp += "\n    ["
        for n, pi in enumerate(self.pi_list):
            tmp +=  f"\n    {n}- {pi} "
        tmp += "\n    ]"
        return tmp
        #return (f'{self.__class__.__name__} = [ ')

    def validate_pi_list(self):
        ''' test if sta[n]+Length/2  <= sta[n+1]-Length/2 
        and that first and last points have L== 0 or L == None '''
        print( "" )
        for n,p in enumerate(self.pi_list):
            print( f'{n}   {type(p)}'  )
        print( "" )

        if  isinstance(self.pi_list[0], pi_point)  and (self.pi_list[0].Length != 0):
            return False
        if  isinstance(self.pi_list[-1], pi_point) and (self.pi_list[-1].Length != 0):
            return False
        for n, pi in enumerate(self.pi_list[1:-1]):
            pi_a = self.pi_list[n]
            pi_b = self.pi_list[n+1]
            if( pi_a.sta + pi_a.Length/2 > pi_b.sta - pi_b.Length/2  ):
                print ( f'Validation Error between sta {pi_a.sta } and {pi_b.sta } ')
                a = pi_a.sta + pi_a.Length / 2
                print ( f'sta + L/2 = {pi_a.sta} + {pi_a.Length} / 2 =  {a}')
                b = pi_b.sta - pi_b.Length / 2
                print ( f'sta + L/2 = {pi_b.sta} - {pi_b.Length} / 2 =  {b}')
                return False
        return True

    def pc_and_pt_list(self):
        ''' no PC or PT's allowed beyond the know PI's'''
        if self.validate_pi_list():   #is it a valid ProG
            self.pc_and_pt_list = []  #empty list to be filled
            for n, pt in enumerate(self.pi_list[0:-1]):
                pi_a = self.pi_list[n]
                pi_b = self.pi_list[n+1]
                delta_elev = pi_b.elev - pi_a.elev
                delta_sta =  pi_b.sta -  pi_a.sta
                grade =  delta_elev / delta_sta
                # pc
                self.pc_and_pt_list.append( dict() )
                self.pc_and_pt_list[-1]['name'] = 'pt' + f"_{n:02d}"
                pc_sta = ( pi_a.sta + pi_a.Length / 2.0)
                pc_elev = pi_a.elev  + grade * pi_a.Length/2.0 
                self.pc_and_pt_list[-1][point] = point(pc_sta, pc_elev)
                self.pc_and_pt_list[-1]['grade']  = grade

                # pt
                self.pc_and_pt_list.append( dict() )
                self.pc_and_pt_list[-1]['name'] = 'pc'+ f"_{n+1:02d}"
                pt_sta  = ( pi_b.sta - pi_b.Length / 2.0)
                pt_elev  = pi_b.elev  - grade * pi_b.Length/2.0
                self.pc_and_pt_list[-1][point] = point(pc_sta, pc_elev)

                self.pc_and_pt_list[-1]['grade']  = grade
            return  self.pc_and_pt_list
'''
    def segments(self):
        # all the  curve segments 
        if self.validate_pi_list():
            self.segments = [] #empty list to be filled.
            # pt_a (sta, elev) L=,  g1=, g2=, r=, pt_b(sta,elev)
            for n, pt in enumerate(self.pi_list[0:-1]):
'''
            

# add a "class point"  and change pi_point to a sub_class
class point:
    def __init__( self, sta=0 , elev= 0 ):
        self.sta  = round(sta, 2)
        self.elev = round(elev, 2)
    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'( sta:{self.sta:.2f}, elev:{self.elev:.2f} )' )

class pi_point(point):
    def __init__( self, sta=0 , elev= 0 , Length = 0 ):
        self.sta = round(sta,0)
        self.elev = round(elev,2)
        self.Length = round(Length,2)
    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'( sta:{self.sta:.2f}, elev:{self.elev:.2f}, Length:{self.Length:.2f} )' )

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key) + ":", end='')
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))



if __name__ == "__main__":
    ''' ProG should start and end with a point with PI's in between '''

    pt_1 = point( 100, 10 )
    pt_2 = pi_point( 200, 0.01, 2 )
    pt_3 = pi_point( 300, 30, 3 )
    pt_4 = point (400, 30 )

    print (dir (pt_1))
    print ( pt_1)
    prl = ProG( "sn", [ pt_1, pt_2, pt_3, pt_4] )
    print( prl.__repr__() )
    print( prl.validate_pi_list() )
    '''
    for j in prl.pc_and_pt_list():
        pretty( j,1 )
        print("")
    pt_4 = point(400, 50)
    print (pt_4)
    '''
