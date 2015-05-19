.PHONY: help test

help:
	@echo
	@echo "USAGE: make [target]"
	@echo
	@echo "TARGETS:"
	@echo
	@echo "  install       - install"
	@echo "  clean         - clean"
	@echo "  test          - run tests"
	@echo "  bench         - run benchmarks"
	@echo "  distribute    - upload to PyPI"
	@echo

test:
	@nosetests test  # --nologcapture

install:
	@python setup.py install

clean:
	@rm -rf build dist nanoservice.egg-info

bench:
	@python benchmarks/bench_req_rep.py
	@python benchmarks/bench_req_rep_auth.py
	@python benchmarks/bench_req_rep_raw.py

	@python benchmarks/bench_pub_sub.py
	@python benchmarks/bench_pub_sub_auth.py
	@python benchmarks/bench_pub_sub_raw.py

distribute:
	@python setup.py register -r pypi && python setup.py sdist upload -r pypi
