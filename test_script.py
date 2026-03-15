import sys

def add(a, b):
    return a + b

def test_add():
    # Intentionally break this by expecting wrong result first
    assert add(2, 2) == 4, "Test failed: 2 + 2 should equal 4"

if __name__ == "__main__":
    try:
        test_add()
        print("All tests passed ✅")
    except AssertionError as e:
        print(f"Test failed ❌: {e}")
        sys.exit(1)  # non-zero exit code → pipeline fails
