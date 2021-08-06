from TopXLoudnessDetector import TopXLoudnessDetector

def main():
    target = TopXLoudnessDetector("../top50.csv")
    target.extract_mp3_from_top_x()


if __name__ == "__main__":
    main()