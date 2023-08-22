import json
from pyspark.sql.functions import explode, col
from pyspark.sql import SparkSession
import findspark
findspark.init()


def write_in_file(filename, data_to_write):
    with open("json_files/"+filename, "w")as outfile:
        data = json.dumps(data_to_write, default=str)
        outfile.write(data)


if __name__ == '__main__':
    spark = SparkSession.builder.appName("AlienVault").getOrCreate()
    indicators_df = spark.read.json("json_files/data.json")
    indicators_df.createOrReplaceTempView("indicators_tv")

    data = spark.sql(
        'select indicators from indicators_tv').collect()

    link_rows = []
    domain_rows = []

    for data_indicators in data:
        for indicators in data_indicators:
            for indicator in indicators:
                if indicator['type'] == "URL":
                    link_rows.append(indicator['indicator'])
                elif indicator['type'] == "domain":
                    domain_rows.append(indicator['indicator'])

    write_in_file("malicious_domains.json", domain_rows)
    write_in_file("malicious_links.json", link_rows)

    spark.stop()
