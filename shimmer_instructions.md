# Shimmer UI Refactoring Plan

We need to implement Skeleton Loaders (Shimmer Effect) for the `BrowseScreen` and `ProfileScreen` in the CacheDeal app. The architecture has changed from Offline-First Room DB to a Cloud-First Supabase Architecture. 

## Requirements:
1. `ShimmerEffect.kt` is already available as a modifier: `Modifier.shimmerEffect()`.
2. Update `BrowseScreen.kt`:
   - Use `remember { mutableStateOf<List<Item>?>(null) }` and a `LaunchedEffect` to fetch `ItemRepository(context).getAllItems()`.
   - While `items == null`, display a grid of 6 placeholder `BrowseItemCard`s.
   - For placeholder cards, apply `Modifier.shimmerEffect()` to the Card's background, and to the text boxes representing title and price.
   - Do NOT use `item.sellerName` or `item.sellerBlock` or `item.createdAt` on `Item` anymore, just use empty strings or "Seller" as placeholders since those properties were removed from `Item.kt`.
3. Update `ProfileScreen.kt`:
   - Use `LaunchedEffect` to fetch `AuthRepository.getCurrentUserProfile()`, `ItemRepository.getMyItems()`, and `DealRepository.getMyDeals()`.
   - While data is loading (null), show shimmering UI for the top section (Avatar, dots) and the list below.
   - Remove usage of `sellerName` and `buyerName` from `DealCard` or stub them out.
4. Ensure the app builds completely without unresolved reference errors.
