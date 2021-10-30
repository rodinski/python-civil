# awk understands  \f as formfeed  use \%x0c for VIM



/^\f Weight/ {
    getline

    #skip all of this page
    while( $0 !~/\f/) { 
        getline
    }
    getline
    #print all of this page
    while ($0 !~/\f/) {

        gsub("Web Spl","WebSpl ")
        print $0
        getline
    }
}

/^\f Shear Stress/ {
    #skip top
    while ($1 != "0"){ 
        getline
    }
    #body so save locations
    while( $0 !~ /^ *$/ && $1 > -1 ){
        loc[$1] = $2
        print loc[$1]
        getline
    }
}



