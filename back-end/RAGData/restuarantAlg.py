restaurantDataSet = ["chaat bhavan", "bjs", "dave's hot chicken", "five guys", "lazy dog", "star chaat", "taco bell"]

restaurantDesc = {
    "chaat bhavan":"Chaat Bhavan is a popular Indian restaurant known for its delicious and authentic street food-inspired dishes. It offers a variety of flavorful chaats, curries, and other traditional Indian delicacies in a vibrant and welcoming atmosphere.",
    "bjs":"bj's restaurant & Brewhouse is a casual dining chain known for its extensive menu that includes deep-dish pizzas, handcrafted beers, and a variety of American comfort foods. With a lively atmosphere and a commitment to quality, BJ's offers a family-friendly dining experience complemented by its signature brews and desserts.",
    "dave's hot chicken":"Dave's Hot Chicken is a trendy fast-casual restaurant specializing in Nashville-style hot chicken, offering various heat levels to cater to all spice preferences. Known for its flavorful and juicy chicken tenders and sliders, Dave's Hot Chicken has quickly gained a cult following for its bold and delicious offerings.",
    "five guys":"Five Guys is a popular fast-casual chain renowned for its customizable burgers, fresh-cut fries, and casual, no-frills dining experience. With a focus on high-quality ingredients and generous portions, Five Guys is celebrated for its straightforward yet delicious approach to classic American fare.",
    "lazy dog":"Lazy Dog Restaurant & Bar offers a relaxed, family-friendly dining experience with a diverse menu that includes comfort food favorites, gourmet burgers, and inventive dishes inspired by American cuisine. The restaurant's cozy atmosphere and dog-friendly policy make it a popular choice for casual dining and social gatherings.",
    "star chaat":"Star Chaat is a vibrant eatery specializing in a wide array of flavorful and authentic Indian street foods, particularly its renowned chaats. With a focus on fresh ingredients and traditional recipes, Star Chaat provides a lively dining experience centered around delicious, savory snacks and appetizers.",
    "taco bell":"Taco Bell is a fast-food chain known for its innovative take on Mexican cuisine, offering a menu that includes tacos, burritos, and nachos. Renowned for its customizable and affordable offerings, Taco Bell provides a quick and casual dining experience with a variety of flavors and unique menu items."
}

print(sorted(restaurantDataSet))

def binary_search_restaurants(restaurants, userRestaurant):
    restaurants = sorted(restaurants)
    left = 0
    right = len(restaurants) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_restaurant = restaurants[mid]

        if mid_restaurant == userRestaurant:
            return mid
        elif mid_restaurant < userRestaurant:
            left = mid + 1
        else:
            right = mid - 1

    return -1

target = input("Enter a restaurant and get it's description: ").lower()

result = binary_search_restaurants(restaurantDataSet, target)

print(restaurantDataSet[result])
print(restaurantDesc.get(restaurantDataSet[result]))