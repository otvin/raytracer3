import unit_tests

def run_tests():
    count = 0

    # some tests take longer and we can skip unless we're explicitly testing a change to that feature.
    # tests_to_skip = ['test_canvas3']
    tests_to_skip = []

    for name, val in unit_tests.__dict__.items():
        if name[:5] == 'test_':
            if name not in tests_to_skip:
                val()
                print ('{} complete'.format(name))
                count += 1
            else:
                print ('{} skipped'.format(name))
    print ('{} tests completed.'.format(count))

if __name__ == '__main__':
    run_tests()
    print('Success!')