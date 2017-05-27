find -name '*.proto'|
	while read file; do 
		package=$(cat $file|sed -En 's/^package (.*);/\1/p')
		cat $file|sed -En "s/^service (.*)\{/${package}.\1/p"
done

