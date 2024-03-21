#!/bin/zsh
brand="gucci"
item="財布"
date=$(date +%Y%m%d)
python get_product_info.py $brand $item
python auto_post_margiela.py $date $brand
