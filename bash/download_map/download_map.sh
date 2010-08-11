#!/bin/bash


y=0
# -11600 - -200
for t in {-11600..-200..200}
do
    x=0
    # 0 - 7200
    for l in {0..7200..200}
    do
        wget -q -O tmp.png -U "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.10) Gecko/20100623 Iceweasel/3.5.10 (like Firefox/3.5.10)" "http://karte.namibia-forum.ch:8080/tracks4africa/tile.php?map=t4a_namibia&t=$t&l=$l&s=2835&g=__base__&i=png24"
        convert +append row.png tmp.png row.png >> /dev/null 2>&1
        rm tmp.png
        #wget -q -O map_$(printf "%04d_%04d" $x $y).png -U "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.10) Gecko/20100623 Iceweasel/3.5.10 (like Firefox/3.5.10)" "http://karte.namibia-forum.ch:8080/tracks4africa/tile.php?map=t4a_namibia&t=$t&l=$l&s=2835&g=__base__&i=png24"
        let x++
    done
    convert -append map.png row.png map.png >> /dev/null 2>&1
    rm row.png
    let y++
done

