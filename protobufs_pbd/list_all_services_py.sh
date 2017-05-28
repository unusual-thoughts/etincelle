imports=()
echo 'all_services = ['
for file in $(find -name '*.proto'); do
	package=$(cat $file|sed -En 's/^package (.*);/\1/p')
	#cat $file|sed -En "s/^service (.*)\{/${package}.\1/p"
	importname=${file%%.proto}
	importname=${importname##./}
	importname=${importname//\//.}_pb2
	#echo "import $importname"
	imports+=("$importname")
	services=$(cat $file|sed -En "s/^service (.*)\{/\1/p")
	
	for service in $services; do
		echo "	{
		\"srv\": ${importname}.${service}(),
		\"name\": \"${package}.${service}\",
	},"
		#echo $service|
		#sed -E 's/(.)([A-Z])/\1_\2/g' |
		#tr 'A-Z' 'a-z'
	done
done
echo ']'
echo ''

#for import in ${imports[@]}; do
#	echo "import ${import}"
#done
