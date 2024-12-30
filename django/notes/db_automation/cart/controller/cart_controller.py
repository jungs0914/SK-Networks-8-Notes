from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status

from cart.service.cart_service_impl import CartServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class CartController(viewsets.ViewSet):
    redisCacheService = RedisCacheServiceImpl.getInstance()
    cartService = CartServiceImpl.getInstance()

    def requestCreateCart(self, request):
        postRequest = request.data
        cart = postRequest.get("cart")
        userToken = postRequest.get("userToken")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)

            updatedCart = self.cartService.createCart(accountId, cart)
            if updatedCart is not None:
                return JsonResponse({"message": "장바구니에 아이템이 추가되었습니다.", "success": True}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"장바구니 처리 중 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestListCart(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        page = postRequest.get("page", 1)
        pageSize = postRequest.get("pageSize", 10)

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)

            cartList, totalItems = self.cartService.listCart(accountId, page, pageSize)
            print(f"cartList: {cartList}, totalItems: {totalItems}")

            return JsonResponse({
                "cartList": cartList,
                "totalItems": totalItems,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

