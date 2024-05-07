# Indian Delivery Service

[![pt-br](https://img.shields.io/badge/language-pt--br-green.svg)](https://github.com/GustavoNascimento98/curry-company/blob/main/README.md)
[![en](https://img.shields.io/badge/language-en-red.svg)](https://github.com/GustavoNascimento98/curry-company/blob/main/README-en.md)

![](img/food_delivery.jpg)


</br>

**Tabela de Conteúdos**

- [1. Business Problem](#1-business-problem)
- [2. Assumptions made for the analysis](#2-assumptions-made-for-the-analysis)
- [3. Planning the solution](#3-planning-the-solution)
- [4. Top 3 Insights](#4-top-3-insights)
- [5. Final Product](#5-final-product)
- [6. Conclusion](#6-conclusion)
- [7. Next Steps](#7-next-steps)

</br>

# 1. Business Problem
    
The Curry Company is a tech company that developed an app connecting restaurants, delivery drivers, and customers. Through this app, users can order meals from any registered restaurant and have them delivered to their doorstep by a registered delivery driver.

The company facilitates transactions between restaurants, delivery drivers, and customers, generating a wealth of data on deliveries, order types, weather conditions, delivery driver ratings, and more. Despite the company's growth in terms of deliveries, the CEO lacks complete visibility into the company's growth KPIs.

You've been hired as a Data Scientist to create data solutions for delivery. However, before training algorithms, the company's need is to have the main strategic KPIs organized in a single tool so that they can easily consult and make important decisions. The Curry Company operates on a Marketplace business model, acting as an intermediary between three main clients: Restaurants, delivery drivers, and customers. To track the growth of these businesses, the CEO would like to see the following growth metrics:

    
****************On the company side:****************

1. Number of orders per day.
2. Number of orders per week.
3. Distribution of orders by traffic type.
4. Comparison of order volume by city and traffic type.
5. Number of orders per delivery driver per week.
6. Central location of each city by traffic type.

</br>

********************************************On the delivery driver side:********************************************

1. The youngest and oldest ages of delivery drivers.
2. The best and worst vehicle conditions.
3. Average rating per delivery driver.
4. Average rating and standard deviation by traffic type.
5. Average rating and standard deviation by weather conditions.
6. Top 10 fastest delivery drivers per city.
6. Top 10 slowest delivery drivers per city.

</br>

**************************************************On the restaurant side:**************************************************

1. Number of unique delivery drivers.
2. Average distance from restaurants to delivery locations.
3. Average delivery time and standard deviation per city.
4. Average delivery time and standard deviation per city and order type.
5. Average delivery time and standard deviation per city and traffic type.
6. Average delivery time during festivals.

The goal of this project is to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.

    
</br>

# 2. Assumptions made for the analysis

1. The analysis was conducted using data between 11/02/2022 and 06/04/2022.

2. Marketplace was the assumed business model.

3. The 3 main business views were:
    1. Order transaction view
    2. Restaurants view
    3. Delivery drivers view


    
</br>
    
# 3. Planning the solution.

The strategic dashboard utilizing metrics reflecting the 3 main views of the company's business model:

1. **Company growth view**:
    - Orders per day.
    - Percentage of orders by traffic conditions.
    - Number of orders by type and city.
    - Orders per week.
    - Number of orders by delivery type.
    - Number of orders by traffic conditions and city type.


2. **Restaurants growth view**:
    - Number of unique orders.
    - Average distance traveled.
    - Average delivery time during festivals and regular days.
    - Standard deviation of delivery time during festivals and regular days.
    - Average delivery time by city.
    - Distribution of average delivery time by city.
    - Average delivery time by order type.


3. **Delivery drivers growth view**:
    - Age of the oldest and youngest delivery driver.
    - Rating of the best and worst vehicle.
    - Average rating per delivery driver.
    - Average rating by traffic conditions.
    - Average rating by weather conditions.
    - Average time of the fastest delivery driver.
    - Average time of the fastest delivery driver by city.
    
</br>

# 4. Top 3 Insights
    
1. The seasonality of the order quantity is daily. There is a variation of approximately 10% in the number of orders on consecutive days.

2. Semi-Urban cities do not have low traffic conditions.

3. The largest variations in delivery time occur during sunny weather.

</br>

# 5. Final Product

The final product is an online dashboard, hosted on a Cloud and available for access on any internet-connected device.

The dashboard can be accessed through this link: [dashboard](https://gustavo-curry-company.streamlit.app/)

</br>

# 6. Conclusion

The goal of this project was to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.

From the company's perspective, we can conclude that the number of orders increased between week 06 and week 13 of the year 2022.


</br>

# 7. Next Steps

1. Reduce the number of metrics.
2. Create new filters.
3. Add new business views.