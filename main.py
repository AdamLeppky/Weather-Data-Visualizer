
import matplotlib.pyplot as plt
from Observations import Observations


def main():
    observations = Observations('68516', 'US', '2020-09-01', '2020-10-20')

    # plt.style.use('seaborn-whitegrid')
    plt.plot(observations.get_temperatures()['timestamps'], observations.get_temperatures()['temperatures'])
    plt.xlabel("Date")
    plt.ylabel("Temperature (°F)")
    plt.title("Temperatures from September 1st, 2020 - October 20th, 2020")
    plt.show()


if __name__ == '__main__':
    main()
