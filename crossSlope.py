print(   dir() )


s = [ {"sta":100, "r":[ (17.33, 6 ), ],  "l":[ (-17.33, 6 ), (-11, 1 ),] },
      {"sta":300, "r":[ (17.33, 6 ), ],  "l":[ (-17.33, 6 ), (-11, 1 ),] },
      {"sta":450, "r":[ (17.33, 2 ), ],  "l":[ (-17.33, 2 ), (-11, 1 ),] },
      {"sta":750, "r":[ (17.33, 0 ), ],  "l":[ (-17.33, 2 ), (-11, 1 ),] },
      {"sta":950, "r":[ (17.33, -2 ), ], "l":[ (-17.33, 2 ), (-11, 1 ),] },
      ]


def  slope_from_sta( station ):
    if station < s[0]["sta"]:
        return "sta out of range too small"
    if station > s[-1]["sta"]:
        return "sta out of range too large"

    for (bk,ah) in zip( s[:-1],s[1:] ):
        print (bk["sta"],  ah["sta"])
        if bk["sta"] < station and station  < ah["sta"]:
            L_sta = ah["sta"] - bk["sta"] 
            x_sta = station - bk["sta"]
            pct = x_sta / L_sta
            
            for b_a in [bk, ah]: 
                for  lr in ["l", "r"]:
                    print ("==start==")
                    for (off, slope) in b_a[lr]:
                        print ( off, slope, lr)
                    print ("== end ==")



            pass
            # get to work here. 

    return 1

#if __name__ == "__main__":
print ( slope_from_sta( 302 ) ) 

print(s)
