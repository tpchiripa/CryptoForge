from cryptoforge.discovery.inference.registry import InferenceRegistry


def main():

    print("Registered Inferencers")
    print("=" * 40)

    print(InferenceRegistry.count())
    print(InferenceRegistry.names())


if __name__ == "__main__":
    main()