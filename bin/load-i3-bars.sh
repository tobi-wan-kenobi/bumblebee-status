#!/usr/bin/env bash

if [ ! -f ~/.config/i3/config.template ]; then
	cp ~/.config/i3/config ~/.config/i3/config.template
else
	cp ~/.config/i3/config.template ~/.config/i3/config
fi

if [ -f ~/.config/i3/config.template.private ]; then
	cat ~/.config/i3/config.template.private >> ~/.config/i3/config
fi

screens=$(xrandr -q|grep ' connected'| grep -P '\d+x\d+' |cut -d' ' -f1)

echo "screens: $screens"

while read -r line; do
	screen=$(echo $line | cut -d' ' -f1)
	others=$(echo $screens|tr ' ' '\n'|grep -v $screen|tr '\n' '-'|sed 's/.$//')

	if [ -f ~/.config/i3/config.$screen-$others ]; then
		cat ~/.config/i3/config.$screen-$others >> ~/.config/i3/config
	else
		if [ -f ~/.config/i3/config.$screen ]; then
			cat ~/.config/i3/config.$screen >> ~/.config/i3/config
		fi
	fi
done <<< "$screens"

i3-msg restart
