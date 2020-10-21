
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import stringcase
from Observations import Observations


def main():
    postal_code = '68516'
    country_code = 'US'
    start_date = '2020-10-10'
    end_date = '2020-10-20'
    observations = Observations(postal_code, country_code, start_date, end_date)

    value_key1 = 'windSpeed'
    title1 = stringcase.titlecase(value_key1)
    metric1 = observations.get_values_by_key(value_key1)
    label1 = title1 + " " + metric1["unit_code"]

    value_key2 = 'windChill'
    title2 = stringcase.titlecase(value_key2)
    metric2 = observations.get_values_by_key(value_key2)
    label2 = title2 + " " + metric2["unit_code"]

    figure(num=None, figsize=(18, 6), dpi=80, facecolor='w', edgecolor='k')

    plt.plot(metric1['timestamps'], metric1['values'], label=label1)
    plt.plot(metric2['timestamps'], metric2['values'], label=label2)

    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title(f"{title1} vs. {title2}\n{postal_code}, {country_code}\nFrom {start_date} to {end_date}")

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
