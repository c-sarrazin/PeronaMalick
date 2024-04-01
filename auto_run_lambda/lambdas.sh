for I in {1..9}
do
	for J in {1..9}
	do
	echo $I $J
	python3 auto_run_lambda/perona_malik_modifie.py $I $J
	done
done
