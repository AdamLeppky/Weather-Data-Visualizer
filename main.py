
import matplotlib.pyplot as plt
import stringcase
from Observations import Observations


def main():
    observations = Observations('68516', 'US', '2020-10-15', '2020-10-20')
    value_key = 'temperature'
    title = stringcase.titlecase(value_key)
    metric = observations.get_values_by_key(value_key)

    plt.style.use('seaborn-whitegrid')
    plt.plot(metric['timestamps'], metric['values'])
    plt.xlabel("Date")
    plt.ylabel(title)
    plt.title(title + " Values")
    plt.show()


if __name__ == '__main__':
    main()
