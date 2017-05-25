for i in {1..5}; do
	cat sess$i.csv| while read line; do
		file=$(echo $line|cut -d, -f3|cut -d/ -f7)
		time=$(echo $line|cut -d, -f2)
		starttime=$(echo $line|cut -d, -f11)
		port=$(echo $line|cut -d, -f5)
		cp "sess$i/$file" "sess$i/$(printf '%08d_%s\n' $(($time - $starttime)) $port).dat"
	done
done
