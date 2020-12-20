import unit_tests

def run_tests():
    count = 0
    for name, val in unit_tests.__dict__.items():
        if name[:5] == 'test_':
            val()
            count += 1
    print ('{} tests completed.'.format(count))

if __name__ == '__main__':
    run_tests()
    print('Success!')