
def pytest_addoption(parser):
    parser.addoption("--foocount",
                     action="store",
                     default=1,
                     type=int,
                     help="run count")

def pytest_generate_tests(metafunc):
    if "foo_count" in metafunc.fixturenames:
        end = metafunc.config.getvalue("foocount")

        def ids(i):
            return f"{i[0]:03d}-{i[1]:03d}"

        def it(count):
            for i in range(count):
                yield i, count
        metafunc.parametrize("foo_count", it(end), ids=ids)
