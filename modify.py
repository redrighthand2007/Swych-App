import os
import re

browse_path = "app/src/main/java/com/kush/cachedeal/ui/browse/BrowseScreen.kt"
with open(browse_path, "r") as f:
    content = f.read()

content = content.replace("import com.kush.cachedeal.core.designsystem.component.CategoryChip",
"""import com.kush.cachedeal.core.designsystem.component.CategoryChip
import com.kush.cachedeal.core.designsystem.component.shimmerEffect""")

content = content.replace("var allItems by remember { mutableStateOf<List<Item>>(emptyList()) }", "var allItems by remember { mutableStateOf<List<Item>?>(null) }")

# In displayItems remember block
old_display = """    val displayItems = remember(selectedCategory, allItems, selectedSort, nearMeEnabled, currentUserBlock) {
        var filtered = if (selectedCategory == null) allItems
        else allItems.filter { it.category == selectedCategory!!.displayName }

        if (nearMeEnabled && currentUserBlock.isNotEmpty()) {
            filtered = filtered.filter { it.sellerBlock == currentUserBlock }
        }

        when (selectedSort) {
            SortOption.RECENT -> filtered.sortedByDescending { it.createdAt }
            SortOption.LOW_TO_HIGH -> filtered.sortedBy { it.price }
            SortOption.HIGH_TO_LOW -> filtered.sortedByDescending { it.price }
        }
    }"""

new_display = """    val displayItems = remember(selectedCategory, allItems, selectedSort, nearMeEnabled, currentUserBlock) {
        if (allItems == null) return@remember null
        var filtered = if (selectedCategory == null) allItems!!
        else allItems!!.filter { it.category == selectedCategory!!.displayName }

        // Seller block filter removed as sellerBlock is not in Item
        // if (nearMeEnabled && currentUserBlock.isNotEmpty()) {
        //     filtered = filtered.filter { it.sellerBlock == currentUserBlock }
        // }

        when (selectedSort) {
            SortOption.RECENT -> filtered // Sort by id or don't sort since createdAt is removed
            SortOption.LOW_TO_HIGH -> filtered.sortedBy { it.price }
            SortOption.HIGH_TO_LOW -> filtered.sortedByDescending { it.price }
        }
    }"""
content = content.replace(old_display, new_display)

# In the Item List section
old_list = """        if (displayItems.isEmpty()) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(text = "📭", style = MaterialTheme.typography.displayMedium)
                    Spacer(Modifier.height(12.dp))
                    Text(
                        text = "No items found",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(
                    items = displayItems,
                    key = { it.id }
                ) { item ->
                    BrowseItemRow(
                        item = item,
                        onClick = {
                            navController.navigate(ItemDetailRoute(item.id))
                        }
                    )
                }
            }
        }"""

new_list = """        if (displayItems == null) {
            // Shimmer Loading State
            LazyColumn(
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(6) {
                    ShimmerBrowseItemRow()
                }
            }
        } else if (displayItems.isEmpty()) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(text = "📭", style = MaterialTheme.typography.displayMedium)
                    Spacer(Modifier.height(12.dp))
                    Text(
                        text = "No items found",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(
                    items = displayItems,
                    key = { it.id }
                ) { item ->
                    BrowseItemRow(
                        item = item,
                        onClick = {
                            navController.navigate(ItemDetailRoute(item.id))
                        }
                    )
                }
            }
        }"""
content = content.replace(old_list, new_list)

# In BrowseItemRow
old_item_row = """                        Text(
                            text = item.sellerName,
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Text(
                            text = item.sellerBlock,
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                        )"""

new_item_row = """                        Text(
                            text = "Seller", // Placeholder since sellerName is removed
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Text(
                            text = "", // Placeholder since sellerBlock is removed
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                        )"""
content = content.replace(old_item_row, new_item_row)

# Append ShimmerBrowseItemRow
shimmer_row = """

@Composable
private fun ShimmerBrowseItemRow() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(100.dp)
            .shimmerEffect(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(modifier = Modifier.fillMaxSize()) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(0.25f)
                    .background(Color.Gray.copy(alpha = 0.3f))
            )

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 12.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                Column {
                    Box(modifier = Modifier.height(16.dp).fillMaxWidth(0.7f).shimmerEffect().background(Color.Gray.copy(alpha = 0.3f)))
                    Spacer(Modifier.height(8.dp))
                    Box(modifier = Modifier.height(14.dp).fillMaxWidth(0.3f).shimmerEffect().background(Color.Gray.copy(alpha = 0.3f)))
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Box(modifier = Modifier.height(12.dp).fillMaxWidth(0.5f).shimmerEffect().background(Color.Gray.copy(alpha = 0.3f)))
                    }
                    Box(modifier = Modifier.height(24.dp).width(60.dp).clip(RoundedCornerShape(6.dp)).shimmerEffect().background(Color.Gray.copy(alpha = 0.3f)))
                }
            }
        }
    }
}
"""
content += shimmer_row

with open(browse_path, "w") as f:
    f.write(content)

# ProfileScreen.kt
profile_path = "app/src/main/java/com/kush/cachedeal/ui/profile/ProfileScreen.kt"
with open(profile_path, "r") as f:
    p_content = f.read()

p_content = p_content.replace("import com.kush.cachedeal.core.designsystem.component.DotBadge",
"""import com.kush.cachedeal.core.designsystem.component.DotBadge
import com.kush.cachedeal.core.designsystem.component.shimmerEffect""")

p_content = p_content.replace("var myItems by remember { mutableStateOf<List<Item>>(emptyList()) }", "var myItems by remember { mutableStateOf<List<Item>?>(null) }")
p_content = p_content.replace("var boughtDeals by remember { mutableStateOf<List<Deal>>(emptyList()) }", "var boughtDeals by remember { mutableStateOf<List<Deal>?>(null) }")
p_content = p_content.replace("var soldDeals by remember { mutableStateOf<List<Deal>>(emptyList()) }", "var soldDeals by remember { mutableStateOf<List<Deal>?>(null) }")

old_deals = """                    if (boughtDeals.isEmpty()) {
                        EmptyListMessage("You haven't bought any items yet.")
                    } else {
                        boughtDeals.forEach { deal ->
                            val dots = counterpartyDots[deal.sellerId]
                            HistoryCard(title = deal.itemTitle, subtitle = "From ${deal.sellerName}", dots = dots)
                        }
                    }"""
new_deals = """                    if (boughtDeals == null) {
                        EmptyListMessage("Loading...")
                    } else if (boughtDeals!!.isEmpty()) {
                        EmptyListMessage("You haven't bought any items yet.")
                    } else {
                        boughtDeals!!.forEach { deal ->
                            val dots = counterpartyDots[deal.sellerId]
                            HistoryCard(title = deal.itemTitle, subtitle = "From Seller", dots = dots)
                        }
                    }"""
p_content = p_content.replace(old_deals, new_deals)

old_sold = """                    if (soldDeals.isEmpty()) {
                        EmptyListMessage("You haven't completed any sales yet.")
                    } else {
                        soldDeals.forEach { deal ->
                            val dots = counterpartyDots[deal.buyerId]
                            HistoryCard(title = deal.itemTitle, subtitle = "Sold to ${deal.buyerName}", dots = dots)
                        }
                    }"""
new_sold = """                    if (soldDeals == null) {
                        EmptyListMessage("Loading...")
                    } else if (soldDeals!!.isEmpty()) {
                        EmptyListMessage("You haven't completed any sales yet.")
                    } else {
                        soldDeals!!.forEach { deal ->
                            val dots = counterpartyDots[deal.buyerId]
                            HistoryCard(title = deal.itemTitle, subtitle = "Sold to Buyer", dots = dots)
                        }
                    }"""
p_content = p_content.replace(old_sold, new_sold)

old_my = """                    if (myItems.isEmpty()) {
                        EmptyListMessage("You haven't listed any items.")
                    } else {
                        myItems.forEach { item ->
                            HistoryCard(title = item.title, subtitle = "₹${item.price}", dots = null)
                        }
                    }"""
new_my = """                    if (myItems == null) {
                        EmptyListMessage("Loading...")
                    } else if (myItems!!.isEmpty()) {
                        EmptyListMessage("You haven't listed any items.")
                    } else {
                        myItems!!.forEach { item ->
                            HistoryCard(title = item.title, subtitle = "₹${item.price}", dots = null)
                        }
                    }"""
p_content = p_content.replace(old_my, new_my)

old_count_bought = "count = boughtDeals.size,"
new_count_bought = "count = boughtDeals?.size ?: 0,"
p_content = p_content.replace(old_count_bought, new_count_bought)

old_count_sold = "count = soldDeals.size,"
new_count_sold = "count = soldDeals?.size ?: 0,"
p_content = p_content.replace(old_count_sold, new_count_sold)

old_count_my = "count = myItems.size,"
new_count_my = "count = myItems?.size ?: 0,"
p_content = p_content.replace(old_count_my, new_count_my)

# "While data is loading (null), show shimmering UI for the top section (Avatar, dots) and the list below."
# If user is null, instead of CircularProgressIndicator, we show a shimmer layout for user.
old_user_null = """    if (user == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
        return
    }"""
new_user_null = """    if (user == null) {
        Column(modifier = Modifier.fillMaxSize()) {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .shimmerEffect(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .weight(0.25f)
                            .aspectRatio(1f)
                            .clip(CircleShape)
                            .background(Color.Gray.copy(alpha = 0.3f))
                    )
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(0.75f)) {
                        Box(modifier = Modifier.height(20.dp).fillMaxWidth(0.6f).background(Color.Gray.copy(alpha = 0.3f)))
                        Spacer(modifier = Modifier.height(8.dp))
                        Box(modifier = Modifier.height(16.dp).fillMaxWidth(0.4f).background(Color.Gray.copy(alpha = 0.3f)))
                        Spacer(modifier = Modifier.height(8.dp))
                        Box(modifier = Modifier.height(16.dp).fillMaxWidth(0.5f).background(Color.Gray.copy(alpha = 0.3f)))
                    }
                }
            }
        }
        return
    }"""
p_content = p_content.replace(old_user_null, new_user_null)

with open(profile_path, "w") as f:
    f.write(p_content)

print("Files modified successfully.")
