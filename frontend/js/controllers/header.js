//контроллер для шапки, подключается в index.html
main.controller('header',function($scope,$http,$location,$cookies){
  
  //функция которая срабатывает при клике бургера
  $scope.burgerClass = function() {
    //если имеет класс deactive то ставим класс active меню, иначе наоборот
    if ( $('.header__menu').hasClass("deactive") ) {
      $('.header__menu').removeClass("deactive")
      $('.header__menu').addClass("active")
    }
    else {
      $('.header__menu').removeClass("active")
      $('.header__menu').addClass("deactive")
    }

    //тоже самое, но без deactive у бургера
    $('.header__burger').toggleClass('active');
    //переключение класса lock для блокирования скролла
    $('body').toggleClass('lock');
  }
  

  //по клику в элементы меню менюшка закрывается
  $scope.close = function() {
    if ( $('.header__menu').hasClass("active") ) {
      $('.header__menu').removeClass("active");
      $('.header__menu').addClass("deactive");
      $('body').toggleClass('lock');
      $('.header__burger').toggleClass('active');
    }
  }
});