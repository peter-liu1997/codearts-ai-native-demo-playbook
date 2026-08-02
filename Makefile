.PHONY: list verify serve clean

list:
	python3 demo.py list

verify:
	python3 demo.py verify

serve:
	python3 demo.py serve --port 8000

clean:
	rm -rf .build

