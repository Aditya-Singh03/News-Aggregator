#!/bin/bash

gh repo list CS520-news-aggregator --limit 4000 | while read -r repo _; do
    if [[ "$repo" == "CS520-news-aggregator/news-aggregator" ||  "$repo" == "CS520-news-aggregator/annotator" ]]; then
        continue
    fi
    echo "Cloning $repo"
    gh repo clone "$repo" -- --recurse-submodules
done
