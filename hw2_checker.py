# coding=utf-8


group_count = 0
pot_count = 0
countries = []
pot_countries = {}
federation_countries = {}


def read_file(filename):
    global group_count, pot_countries, countries, pot_countries, federation_countries
    input_file = open(filename, "r")

    group_count = int(input_file.readline().replace("\n", ""))
    pot_count = int(input_file.readline().replace("\n", ""))

    pot_countries = {}
    federation_countries = {}

    for i in range(1, pot_count + 1):
        pot_countries[i] = input_file.readline().replace("\n", "").split(",")
    for i in range(1, 7):  # hard coding the number of continents as specified in the input
        federation_country_mapper = input_file.readline().replace("\n", "").partition(":")
        federation_countries[federation_country_mapper[0]] = federation_country_mapper[2].split(",") \
            if federation_country_mapper[2] != "None" else []

    countries = []
    for pot in pot_countries:
        countries.extend(pot_countries[pot])
    # TODO: Check if sort is needed before assigning the numbers to the lists
    countries.sort()

    input_file.close()


def read_output_file(filename):
    group_allocation = {}
    with open(filename, "r") as output_file:
        decision = output_file.readline().replace("\n", "").split(",")
        if decision == "No":
            print "No mapping possible"
        else:
            country_mapper = {}
            for i in range(0, group_count):
                group_allocation[i] = output_file.readline().replace("\n", "").split(",")
                if len(group_allocation[i]) != 0 and group_allocation[i][0] != "None":
                    for c in group_allocation[i]:
                        country_mapper[c] = i
            for p in pot_countries:
                p_set = set()
                for c in pot_countries[p]:
                    if c not in country_mapper:
                        print c, " is not assigned group"
                        return
                    p_set.add(country_mapper[c])
                if len(p_set) != len(pot_countries[p]):
                    print "same group for countries from same pot"

            for f in federation_countries:
                f_set = {}
                for c in federation_countries[f]:
                    if country_mapper[c] in f_set:
                        f_set[country_mapper[c]] += 1
                    else:
                        f_set[country_mapper[c]] = 1
                if f != "UEFA":
                    for k in f_set:
                        if f_set[k] > 1:
                            print "same group for countries from same federation not UEFA"
                else:
                    for k in f_set:
                        if f_set[k] > 2:
                            print "same group for countries from same federation UEFA"


read_file("input.txt")
read_output_file("output.txt")
