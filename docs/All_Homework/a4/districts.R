##############################################################################################################
####################################### 1. Ingesting data ####################################################
##############################################################################################################

library(tidyverse)
# districts.csv contains demographic information and characteristics 
# about the districts where customers and branches are located.
districts <- read_csv("data/districts.csv")


##############################################################################################################
####################################### 2. Cleaning data #####################################################
##############################################################################################################

### 2.2 clean dataset: districts
glimpse(districts)


num_col = c("Population500", "Population500to1999", "Population2000to9999", "Population10000",
            "unemployment_rate_1995", "unemployment_rate_1996",
            "commited_crimes_1995", "commited_crimes_1996")

# separate values in columns $municipality_info, $unemployment_rate, $commited_crimes into different columns
districts_r <- districts %>%
  separate(municipality_info,
           into = c("Population500", "Population500to1999", "Population2000to9999", "Population10000"),
           sep = ",") %>%
  separate(unemployment_rate,
           into = c("unemployment_rate_1995", "unemployment_rate_1996"),
           sep = ",") %>%
  separate(commited_crimes,
           into = c("commited_crimes_1995", "commited_crimes_1996"),
           sep = ",") %>%
  # below comment is to replace [ in a single column, 
  # but mutate_all & replace_all replace [ in the entire dataframe
  #mutate(Population500 = str_replace(Population500, "\\[", "")) %>%
  #mutate(Population500 = str_replace(Population500, "\\[", ""))
  mutate_all(funs(str_replace_all(., "\\[", ""))) %>%
  mutate_all(funs(str_replace_all(., "\\]", "")))
  # convert strings into numeric, but not time consuming, using sapply instead
  # mutate(Population500 <- as.numeric(Population500)) %>%
  # mutate(Population500to1999 <- as.numeric(Population500to1999)) %>%
  # mutate(Population2000to9999 <- as.numeric(Population2000to9999)) %>%
  # mutate(Population10000 <- as.numeric(Population10000)) %>%
  # mutate(unemployment_rate_1995 <- as.numeric(unemployment_rate_1995)) %>%
  # mutate(unemployment_rate_1996 <- as.numeric(unemployment_rate_1996)) %>%
  # mutate(commited_crimes_1995 <- as.numeric(commited_crimes_1995)) %>%
  # mutate(commited_crimes_1996 <- as.numeric(commited_crimes_1996))

  # convert strings into numeric
districts_r[num_col] <- sapply(districts_r[num_col],as.numeric)
sapply(districts_r, class)

districts_r %>% glimpse()

# remove [ & ] by replacing it with blank
# below works on a single column
# districts_r$Population500 <- gsub("\\[", "", districts_r$Population500)

write.csv(districts_r, "districts_r.csv")
