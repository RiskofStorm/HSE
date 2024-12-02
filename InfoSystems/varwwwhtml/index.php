```
<?php
$username = 'Данил Абрамов';
echo <<<MYHTML
<!DOCTYPE html>
<html>
<head>
<title>Моя первая страница</title>
</head>
<body>
<h1>Привет, $username! Я заголовок</h1>
<p style="color:blue">Я текст страницы. Используйте <a
href=”https://ya.ru”>Яндекс</a>, чтобы разобраться, что делать дальше.</p>
<script>
document.querySelector('h1').onclick = function() {
alert('Домашнее задание выполнено!');
}
</script>
</body>
</html>
MYHTML;
?>
```