imports=()
echo 'all_msgs = {'
for file in $(find -name '*.proto'); do
	package=$(cat $file|sed -En 's/^package (.*);/\1/p')
	#cat $file|sed -En "s/^message (.*)\{/${package}.\1/p"
	importname=${file%%.proto}
	importname=${importname##./}
	importname=${importname//\//.}_pb2
	#echo "import $importname"
	imports+=("$importname")
	messages=$(cat $file|sed -En "s/^message (.*)\{/\1/p")
	
	for message in $messages; do
		echo "	[
		\"msg\": ${importname}.${message}(),
		\"name\": \"${package}.${message}\",
	],"
		#echo $message|
		#sed -E 's/(.)([A-Z])/\1_\2/g' |
		#tr 'A-Z' 'a-z'
	done
done
echo '}'
echo ''

for import in ${imports[@]}; do
	echo "import ${import}"
done
