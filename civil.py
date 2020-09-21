import random

def format_STA( in_sta, decimal_round = 2 ):
    if (in_sta <  0): 
        return "Negative STA"
    in_sta =  round(in_sta, decimal_round ) 
    whole_sta = int( in_sta / 100 )
    plus_ft    = ( in_sta % 100 )
    return f"{whole_sta:d}+{plus_ft:0{3+decimal_round}.{decimal_round}f}"

#==========================================================
def parse_ft_in(s):
    pos_neg = 1
    s = s.strip()
    if s[0] == '-':
        pos_neg = -1
        s = s[1:]
        s = s.strip()
    in_chr = s.split()
    print( in_chr )
    in_chr = list(  map(  int  , in_chr) )
    if (len(in_chr) == 4):
        ft_dec = in_chr[0] + (in_chr[1] +  (in_chr[2] / in_chr[3] ))/12.0
        return pos_neg * ft_dec
    elif (len(in_chr) == 2):
        ft_dec = in_chr[0] + in_chr[1] /12.0
        return  pos_neg * ft_dec
    else:
        return "parsing error"
        
def gcd( u, v):
    while v:
        u, v = v, u % v
    return abs(u)

def myround(x, prec=2, base=.05):
  '''  usage myround(ft_dec, prec=5, base = 1 /12/denom) '''
  return round(base * round(float(x)/base),prec)

def wrap_with_parens(instring):
    return  "(" + instring[1:-1] + ")"

def remove_spa_spa(instring):
    import re
    return re.sub(r' +',' ',instring)

def feet2callout(ft_dec, denom = 16, 
        option = {   'ft': '{ft:2d}'
                    , 'in':'{in: 2d}' 
                    , 'reduce': True
                    , 'negative': wrap_with_parens
                    } ):
    ''' decimal of a ft to a ( #'-# ##/##")  callout

        once i have ft in numerator and denom 
        i sould call a class(str) and do the formating inside it??

        how
    '''
    sign = 1
    if ft_dec < 0: sign = -1

    
    ft_dec = abs(ft_dec)  #only deal with possitives at this point
    ft = int(ft_dec)
    inch_dec = (ft_dec % 1) * 12  #inchs as decimal
    
    nths =  round( inch_dec * denom) # how man denom (16th) of an inch
    if nths == 12 * denom:
        # deal with  11-16/16"  ie  12*16 nths
        #ft goes up to next whole foot
        ft = ft + 1
        inch = 0
        numerator = 0
    else:
        # general case
        inch = int(nths / denom)
        numerator = nths - (inch * denom)
        if option['reduce']:
            great_commom_devisor = gcd( numerator, denom)
            numerator = int(numerator / great_commom_devisor)
            denom = int(denom / great_commom_devisor) 
    
    #very small negatives are 0.0  not -0.0
    if (ft + inch + numerator == 0): sign=1
    new_dec = round(sign*(ft + (inch + numerator / denom)/12.0),5)
    ts =" "
    if ft == 0:
        ts = " 0'-"
    else: ts = "{0: 3d}'-".format(ft)
    ts += "{0:>2d} ".format(inch) 
    if numerator != 0:
        ts +=  " {0:>2d}/{1:>2d}\" ".format(numerator, denom)
    else:
        ts += '"       '
    if sign == -1:
        ts = option['negative'](ts)
    #return [ new_dec, ft, inch, numerator, denom ]
    return ts

def slope_camber (sta, s1,  e1,   s2, e2,  delta_mid):
    ''' returns the elvation due to beam slope WITH a midspan camber 
    '''
    if (sta < s1 or sta > s2):
        print( "Station is out of range in slope_camber")
    L           = s2 - s1
    rate        = (  e2 - e1 ) / L
    delta_chord = ( sta - s1 ) * rate
    s_mid       = (s2 + s1) / 2
    delta_camber = ( abs( sta - s_mid) / (L / 2.0) ) **2 * delta_mid
    return e1 + delta_chord + ( delta_mid - delta_camber ) 

def bar_area(size): 
    size = int(size)
    if size == 3     :return 0.11
    elif size == 4   :return 0.2  
    elif size == 5   :return 0.31 
    elif size == 6   :return 0.44 
    elif size == 7   :return 0.6  
    elif size == 8   :return 0.79 
    elif size == 9   :return 1    
    elif size == 10  :return 1.27 
    elif size == 11  :return 1.56 
    elif size == 14  :return 2.25 
    elif size == 18  :return 4    
    else:             return "NA"

def bar_wt(size):
    size = int(size)
    if   size ==  3 : return 0.38
    elif size ==  4 : return 0.67
    elif size ==  5 : return 1.04
    elif size ==  6 : return 1.50
    elif size ==  7 : return 2.04
    elif size ==  8 : return 2.67
    elif size ==  9 : return 3.40
    elif size ==  10: return 4.30
    elif size ==  11: return 5.31
    elif size ==  14: return 7.65
    elif size ==  18: return 13.60
    else            : return "NA"
  
if __name__ ==  '__main__':
    pass
    from collections import Counter
    from matplotlib import pyplot as plt
    s1 = 0
    s2 = 20
    e1 = 100
    e2 = 100
    c  = 0.75
    y = []
    s = []
    for sta in range (s1, s2+1):
        sc = slope_camber ( sta, s1, e1, s2, e2, c)
        s.append(sta)
        y.append(sc)
        print(f"elevation: {sc}")
    print( bar_area(11) )
    print( bar_wt(11) )
    plt.plot( s, y, 'ro')
    plt.show()



#==========================================================

'''

#--------------------------------
#
#Alias   ftc goes to feet2callout
no warnings;
*ftc = \&feet2callout;
use warnings; 
#--------------------------------
#
#
'''
'''
sub slope_camber{
        # input list = (sta_of_interest,  sta_brg_1,  e1,   sta_brg_2, e2,  mid_span_camber)
        # returns the elvation due to beam slope WITH camber 
        my $s = shift @_;
        my $s1 = shift @_;
        my $e1 = shift @_;
        my $s2 = shift @_;
        my $e2 = shift @_;
        my $delta_mid = shift @_;
        if ($s < $s1 || $s > $s2) {return "ng"}
        my $L = $s2 - $s1;
        my $rate = ($e2-$e1) / $L;
        my $delta_chord = ($s - $s1) * $rate;
        my $s_mid = ($s2 + $s1) / 2;
        my $delta_camber = (abs($s - $s_mid) / ($L/2.0))**2.0 * $delta_mid;
        return $e1 +  $delta_chord + ($delta_mid - $delta_camber);
}

#--------------------------------
#



sub plateslopes {
        # need to read in numbers here
        # code writen by Jonathan Kuchem 2018_06_11
        #
        # need all info for the following points
        # start - normally a web splice or bearing location
        # end   - normally a web splice or bearing location
        #         a chord will be struck b/w start and end
        #         (mathmatically and likely also in the shop)
        # poi  = point of interest= location to find verticallity
        #
        # Web_ht = needed to turn the angle from vertical into a offset
        #
        
# Function of start, end, point of interest (poi), A, and B
# A and B are known points close to the poi to calculate slope
# Web_ht should be the input of web height for calculating the offset


# Deck Slope Calculations
=pod

    my $s_a =   ($A->{deck} - $poi->{deck})/
                ($A->{d_along} - $poi->{d_along});

    my $s_b =   ($poi->{deck} - $B->{deck})/
            ($poi->{d_along} - $B->{d_along});

    my $s1 =    ($s_a + $s_b)/2;

# Deflection Slope Calculations
    my $ds_a =  (($A->{total_DL} - $poi->{total_DL})/12)/
                ($A->{d_along} - $poi->{d_along});

    my $ds_b =  (($poi->{total_DL} - $B->{total_DL})/12)/
                ($poi->{d_along} - $B->{d_along});

    my $ds1 =   ($ds_a + $ds_b)/2;

    // Offset Calculation

    my $offset =        $Web_ht * ($s1 + $ds1);

    print "Offset :" .nearest (0.0001,$offset);
=cut
}


'''
