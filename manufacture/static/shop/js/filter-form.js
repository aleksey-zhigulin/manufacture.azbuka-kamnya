(function() {
    'use strict';

//module: django.shop, TODO: move this into a summary JS file
    var djangoShopModule = angular.module('django.shop.filter', []);

// Directive <form shop-product-search ...> to be used in the form containing the input field
// for entering the search query
    djangoShopModule.directive('shopProductFilter', ['$window', '$location', function($window, $location) {
        return {
            require: 'form',
            restrict: 'AC',
            controller: ['$scope', '$timeout', function($scope, $timeout) {
                var acPromise = null;

                // handle filter
                $scope.filter = function() {
                    var config;
                    if ($scope.property_filters.length == 0) {
                        config = null;
                        $location.search({});
                    } else {
                        config = {params: {}};
                        for(var key in $scope.property_filters) {
                            for(var value in $scope.property_filters[key]) {
                                if ($scope.property_filters[key][value]){
                                    if (!(key in config.params)) {config.params[key] = [];}
                                    config.params[key].push($scope.property_filters[key][value]);
                                }
                            }
                        }
                        $location.search(config.params);
                    }
                    // delay the execution of reloading products
                    if (acPromise) {
                        $timeout.cancel(acPromise);
                        acPromise = null;
                    }
                    acPromise = $timeout(function() {
                        $scope.$emit('shopCatalogFilter', config.params);
                    }, 666);
                };

            }],
            link: function(scope, element, attrs, formController) {
                var i, splitted, queries = {params: $location.search()};
                // convert query string from URL to object
                if (angular.equals({}, queries.params)) {
                    scope.property_filters = {};
                    queries = $window.location.search.replace(/^\?/, '').split('&');
                    for (i = 0; i < queries.length; i++) {
                        splitted = queries[i].split('=');
                        var param = splitted[0];
                        if (param) {
                            var input = $("input[ng-true-value=\"'" + decodeURIComponent(splitted[1]) + "'\"]");
                            var key = input.attr('ng-model').split('.')[2];
                            var value  = input.attr("ng-true-value").slice(1, -1);
                            if (!(param in scope.property_filters)) {
                                scope.property_filters[param] = {};
                            }
                            scope.property_filters[param][key] = value;
                        }
                    }
                } else {
                    scope.property_filters = {};
                    for (var param in queries.params) {

                        for (var i in queries.params[param]) {
                            var value;
                            if (typeof queries.params[param] === 'string') {
                                value = queries.params[param];
                            } else {
                                value = queries.params[param][i];
                            }

                            var input = $("input[ng-true-value=\"'" + decodeURIComponent(value) + "'\"]");
                            var key = input.attr('ng-model').split('.')[2];
                            var value  = input.attr("ng-true-value").slice(1, -1);
                            if (!(param in scope.property_filters)) {
                                scope.property_filters[param] = {};
                            }
                            scope.property_filters[param][key] = value;
                            if (typeof queries.params[param] === 'sting') {
                                break;
                            }
                        }
                    }
                    scope.filter();
                }

                // handle classic search submission through form
                scope.submitSearch = function() {
                    if (scope.searchQuery.length > 1) {
                        element[0].submit();
                    }
                };

            }
        };
    }]);

})();
