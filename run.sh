#!/bin/zsh
brand="margiela"
date=$(date +%Y%m%d)
python get_product_info.py $brand
python auto_post_margiela.py $date $brand
python create_insta_feed.py $date $brand
