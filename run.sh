#!/bin/zsh
brand="vuitton"
item="財布"
date=$(date +%Y%m%d)
python get_product_info.py $brand $item
python auto_post_margiela.py $date $brand
python create_insta_feed.py $date $brand
