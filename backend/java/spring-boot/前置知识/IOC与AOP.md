# IOC & AOP 系统学习教程（Spring Boot 实战版）
本教程完全贴合Java后端实际开发，从「痛点→原理→手动实现→实战用法→底层原理→避坑指南」循序渐进，学完你不仅能彻底搞懂IOC/AOP，还能直接在项目中落地使用。

> 前置要求：你已掌握Java基础、注解、反射，会用Spring Boot搭建项目

---

## 第一部分：IOC（控制反转）—— Spring的核心基石
### 一、先搞懂：为什么我们需要IOC？
#### 1. 没有IOC的「痛苦代码」
我们以最常见的用户业务为例，模拟传统开发的写法：
```java
// 数据访问层
public class UserDao {
    public void addUser() {
        System.out.println("添加用户到数据库");
    }
}

// 业务层
public class UserService {
    // 手动创建依赖对象
    private UserDao userDao = new UserDao();
    
    public void addUser() {
        userDao.addUser();
    }
}

// 控制层
public class UserController {
    // 手动创建依赖对象
    private UserService userService = new UserService();
    
    public void addUser() {
        userService.addUser();
    }
}
```

这段代码有3个致命问题：
1.  **强耦合**：如果要把`UserDao`换成`UserDaoMyBatisImpl`，所有用到`new UserDao()`的地方都要改，代码量越大越崩溃
2.  **对象冗余**：每个类里都`new`一次`UserDao`，会创建大量重复对象，浪费内存
3.  **测试困难**：单元测试时，无法轻松替换`UserDao`为模拟对象（Mock），依赖硬编码死了

#### 2. 用IOC思想解决问题
IOC的核心是**控制反转**：把「对象的创建、依赖管理、生命周期」的控制权，从程序员手里，反转给「IOC容器」。

你不用再手动`new`对象了，只需要告诉容器：哪些类需要交给你管理，哪些类需要注入依赖，容器会自动帮你完成所有事情。

### 二、核心概念澄清（必懂，避免面试踩坑）
| 概念 | 通俗解释 | 本质 |
|------|----------|------|
| IOC（控制反转） | 一种**设计思想**，不是具体技术 | 解耦对象的创建和使用 |
| DI（依赖注入） | IOC思想的**具体实现方式** | 容器自动把依赖的对象塞给你，不用自己找 |
| IOC容器 | Spring实现IOC/DI的载体 | 一个存所有被管理对象的「大Map」，帮你创建、管理、销毁对象 |
| Bean | 被IOC容器管理的对象 | 容器里的一个个实例 |

> 面试高频误区：IOC不等于DI！IOC是思想，DI是实现这个思想的手段，Spring用DI实现了IOC。

### 三、手动实现极简IOC容器（10分钟彻底搞懂底层）
IOC的底层本质就是「注解+反射+工厂模式」，我们手写一个极简版本，彻底打破它的神秘感。

#### 1. 先定义两个核心注解
```java
// 标记类要交给容器管理
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Component {
}

// 标记要注入的依赖
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Autowired {
}
```

#### 2. 编写业务类，加上注解
```java
@Component
public class UserDao {
    public void addUser() {
        System.out.println("添加用户到数据库");
    }
}

@Component
public class UserService {
    // 自动注入，不用new
    @Autowired
    private UserDao userDao;

    public void addUser() {
        userDao.addUser();
    }
}
```

#### 3. 实现IOC容器核心逻辑
```java
public class SimpleIocContainer {
    // 容器核心：存所有Bean的Map
    private final Map<String, Object> beanMap = new HashMap<>();

    // 容器启动：扫描包、创建Bean、注入依赖
    public void init(String packageName) throws Exception {
        // 1. 扫描包下所有加了@Component的类
        List<Class<?>> classList = scanPackage(packageName);
        
        // 2. 实例化所有Bean，放入容器
        for (Class<?> clazz : classList) {
            Object instance = clazz.getDeclaredConstructor().newInstance();
            beanMap.put(toLowerCaseFirst(clazz.getSimpleName()), instance);
        }
        
        // 3. 依赖注入：给所有@Autowired的字段赋值
        for (Object bean : beanMap.values()) {
            Field[] fields = bean.getClass().getDeclaredFields();
            for (Field field : fields) {
                if (field.isAnnotationPresent(Autowired.class)) {
                    // 从容器里拿到对应的Bean
                    Object dependency = beanMap.get(toLowerCaseFirst(field.getType().getSimpleName()));
                    // 反射给字段赋值
                    field.setAccessible(true);
                    field.set(bean, dependency);
                }
            }
        }
    }

    // 从容器里获取Bean
    public Object getBean(String beanName) {
        return beanMap.get(beanName);
    }

    // 工具方法：首字母小写
    private String toLowerCaseFirst(String str) {
        return Character.toLowerCase(str.charAt(0)) + str.substring(1);
    }

    // 工具方法：扫描包下的类（简化版）
    private List<Class<?>> scanPackage(String packageName) throws Exception {
        // 实际开发中会完整实现包扫描，这里简化，直接返回我们的业务类
        List<Class<?>> classList = new ArrayList<>();
        classList.add(UserDao.class);
        classList.add(UserService.class);
        return classList;
    }
}
```

#### 4. 测试我们的IOC容器
```java
public class Test {
    public static void main(String[] args) throws Exception {
        // 启动容器
        SimpleIocContainer container = new SimpleIocContainer();
        container.init("com.example");
        
        // 从容器里拿Bean，不用自己new
        UserService userService = (UserService) container.getBean("userService");
        userService.addUser(); // 正常执行，输出：添加用户到数据库
    }
}
```

你看，Spring的IOC核心逻辑就是这么简单：启动时扫描注解，通过反射创建对象，再通过反射给依赖字段赋值，把所有对象都存在容器里，用的时候直接拿。

### 四、Spring Boot 中IOC的实战用法（开发必用）
Spring Boot已经把IOC容器完全封装好了，我们不用自己写容器，直接用注解就能实现所有功能。

#### 1. 第一步：把类交给IOC容器管理（Bean注册）
Spring提供了多种方式注册Bean，最常用的有以下几种：

##### 方式1：组件扫描注解（最常用）
在类上加上以下注解，Spring启动时会自动扫描并注册为Bean：
| 注解 | 适用场景 | 说明 |
|------|----------|------|
| `@Component` | 通用组件 | 所有需要交给容器管理的类都可以用 |
| `@Service` | 业务层 | 继承自@Component，语义化，用于Service层 |
| `@Controller` / `@RestController` | 控制层 | 继承自@Component，用于接口层 |
| `@Repository` | 数据访问层 | 继承自@Component，用于Dao/Mapper层 |

示例：
```java
// 业务层，交给容器管理
@Service
public class UserService {
}

// 控制层，交给容器管理
@RestController
public class UserController {
}
```

##### 方式2：@Bean + @Configuration（手动注册）
用于第三方类、需要自定义配置的类，比如RestTemplate、RedisTemplate等：
```java
// 配置类，Spring会自动扫描
@Configuration
public class AppConfig {
    
    // 把方法返回的对象注册到容器里
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplateBuilder()
                .setConnectTimeout(Duration.ofSeconds(5))
                .build();
    }
}
```

#### 2. 第二步：依赖注入（从容器里拿Bean，赋值给需要的字段）
Spring提供了3种注入方式，**优先使用构造器注入**（Spring官方推荐）：

##### 方式1：构造器注入（推荐，生产环境首选）
```java
@Service
public class UserService {
    private final UserDao userDao;

    // 构造器：Spring会自动从容器里找到UserDao注入进来
    // Spring 4.3+：如果只有一个构造器，不用加@Autowired
    public UserService(UserDao userDao) {
        this.userDao = userDao;
    }
}
```
优点：
- 依赖不可变（final修饰）
- 依赖明确，必须传入构造器才能创建对象
- 完全避免循环依赖问题
- 方便单元测试

##### 方式2：@Autowired字段注入（最常用，适合简单场景）
```java
@RestController
public class UserController {
    // 按类型注入：Spring从容器里找到UserService，赋值给这个字段
    @Autowired
    private UserService userService;
}
```

如果同一个类型有多个Bean，用`@Qualifier`指定Bean名称：
```java
@Autowired
@Qualifier("userDaoMyBatisImpl") // 指定Bean的名称
private UserDao userDao;
```

##### 方式3：setter方法注入（极少用）
```java
@Service
public class UserService {
    private UserDao userDao;

    @Autowired
    public void setUserDao(UserDao userDao) {
        this.userDao = userDao;
    }
}
```

#### 3. 进阶：Bean的作用域
用`@Scope`注解指定Bean的生命周期，默认是`singleton`单例：
| 作用域 | 说明 | 适用场景 |
|--------|------|----------|
| `singleton`（默认） | 容器中只有一个实例，全局唯一 | 绝大多数无状态的Bean（Service、Controller、Dao） |
| `prototype` | 每次获取Bean，都创建一个新实例 | 有状态的Bean，每次使用都需要新对象 |
| `request` | 每个HTTP请求创建一个实例 | Web项目，请求级别的Bean |
| `session` | 每个会话创建一个实例 | Web项目，会话级别的Bean |

示例：
```java
// 多例Bean
@Component
@Scope("prototype")
public class RequestContext {
}
```

#### 4. 进阶：Bean的生命周期
Spring管理Bean的完整流程，我们可以通过注解介入生命周期：
1.  容器启动，扫描类，创建Bean实例
2.  注入依赖（DI）
3.  执行初始化方法（`@PostConstruct`标记的方法）
4.  Bean可以正常使用
5.  容器关闭，执行销毁方法（`@PreDestroy`标记的方法）

示例：
```java
@Service
public class UserService {
    @PostConstruct
    public void init() {
        System.out.println("Bean初始化完成，执行这里");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("容器关闭，Bean销毁，执行这里");
    }
}
```

### 五、IOC核心好处总结
1.  **彻底解耦**：对象的创建和使用分离，换实现类不用改业务代码
2.  **统一管理**：单例Bean由容器统一管理，避免对象冗余，节省内存
3.  **方便测试**：可以轻松注入Mock对象，单元测试更简单
4.  **降低开发成本**：不用关心对象的创建、依赖关系，专注业务逻辑

---

## 第二部分：AOP（面向切面编程）—— 业务解耦的神器
### 一、先搞懂：为什么我们需要AOP？
#### 1. 没有AOP的「痛苦代码」
我们开发中，经常会遇到一些和**核心业务无关**，但又必须在很多地方写的代码，比如：
- 接口请求日志（入参、出参、耗时）
- 权限校验
- 事务管理
- 接口限流
- 异常统一处理

没有AOP的时候，我们只能这么写：
```java
@RestController
public class UserController {
    @Autowired
    private UserService userService;

    @PostMapping("/add")
    public void addUser(User user) {
        // 1. 日志：记录请求开始时间
        long start = System.currentTimeMillis();
        // 2. 权限校验：判断用户是否有权限
        if (!hasPermission()) {
            throw new RuntimeException("无权限");
        }
        try {
            // 3. 核心业务代码
            userService.addUser(user);
            // 4. 日志：记录成功日志
            System.out.println("添加用户成功");
        } catch (Exception e) {
            // 5. 异常处理
            System.out.println("添加用户失败：" + e.getMessage());
            throw e;
        } finally {
            // 6. 日志：记录接口耗时
            System.out.println("接口耗时：" + (System.currentTimeMillis() - start) + "ms");
        }
    }
}
```

这段代码的问题非常明显：
1.  **代码冗余**：每个接口都要写日志、权限、异常处理，重复代码满天飞
2.  **业务污染**：核心业务代码被大量非业务代码淹没，可读性极差
3.  **维护困难**：要改日志格式，所有接口都要改，工作量巨大

#### 2. 用AOP思想解决问题
AOP的核心是**面向切面编程**：把「与核心业务无关、重复执行的横切逻辑」抽离出来，统一管理，在不修改业务代码的前提下，给业务方法增强功能。

- 正常的业务代码是**纵向执行**：Controller → Service → Dao
- AOP是**横向切入**：在所有业务方法的前后、异常时，统一执行横切逻辑

### 二、AOP核心概念（必懂，不然会懵）
我们用「给所有接口加耗时统计」的例子，把所有概念讲透：
| 概念 | 通俗解释 | 对应例子 |
|------|----------|----------|
| 切面（Aspect） | 抽离出来的横切逻辑类，里面定义切入点和通知 | 日志切面类`LogAspect` |
| 连接点（JoinPoint） | 可以被切入的位置，Spring中只支持方法执行 | 所有Controller的方法 |
| 切入点（Pointcut） | 具体要切入哪些方法，用表达式筛选 | 切入`com.example.controller`包下的所有方法 |
| 通知（Advice） | 具体要执行的代码，以及在方法的什么时机执行 | 记录耗时的代码，在方法执行前后执行 |
| 目标对象（Target） | 被切入的对象，也就是业务对象 | UserController |
| 代理对象（Proxy） | AOP底层生成的动态代理对象，执行通知+目标方法 | Spring自动生成的UserController代理对象 |
| 织入（Weaving） | 把切面逻辑应用到目标对象，生成代理对象的过程 | Spring启动时自动完成 |

### 三、手动实现极简AOP（10分钟搞懂底层）
AOP的底层本质就是**动态代理**，我们用JDK动态代理手写一个极简AOP，彻底打破神秘感。

#### 1. 先定义业务接口和实现类
```java
// 业务接口
public interface UserService {
    void addUser();
}

// 业务实现类（目标对象）
@Service
public class UserServiceImpl implements UserService {
    @Override
    public void addUser() {
        System.out.println("核心业务：添加用户");
    }
}
```

#### 2. 定义切面类（横切逻辑）
```java
public class LogAspect {
    // 前置通知：方法执行前执行
    public void before() {
        System.out.println("前置通知：记录方法开始时间");
    }

    // 后置通知：方法执行后执行
    public void after() {
        System.out.println("后置通知：记录方法耗时");
    }
}
```

#### 3. 用JDK动态代理实现AOP
```java
public class AopProxyFactory implements InvocationHandler {
    // 目标对象（被代理的业务对象）
    private final Object target;
    // 切面类
    private final LogAspect aspect = new LogAspect();

    public AopProxyFactory(Object target) {
        this.target = target;
    }

    // 生成代理对象
    public Object getProxyInstance() {
        return Proxy.newProxyInstance(
                target.getClass().getClassLoader(),
                target.getClass().getInterfaces(),
                this
        );
    }

    // 执行代理逻辑
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 执行前置通知
        aspect.before();
        long start = System.currentTimeMillis();
        Object result;
        try {
            // 执行目标方法
            result = method.invoke(target, args);
        } finally {
            // 执行后置通知
            long end = System.currentTimeMillis();
            System.out.println("方法耗时：" + (end - start) + "ms");
            aspect.after();
        }
        return result;
    }
}
```

#### 4. 测试我们的AOP
```java
public class Test {
    public static void main(String[] args) {
        // 目标对象
        UserService target = new UserServiceImpl();
        // 生成代理对象
        UserService proxy = (UserService) new AopProxyFactory(target).getProxyInstance();
        // 执行代理方法
        proxy.addUser();
    }
}
```

执行结果：
```
前置通知：记录方法开始时间
核心业务：添加用户
方法耗时：1ms
后置通知：记录方法耗时
```

你看，AOP的核心就是动态代理：不修改目标类的代码，通过代理对象，在方法执行前后插入我们的横切逻辑。

### 四、Spring Boot 中AOP的实战用法（开发必用）
Spring Boot已经把AOP完全封装好了，我们不用自己写动态代理，几行注解就能实现强大的AOP功能。

#### 1. 第一步：引入依赖
在`pom.xml`中引入AOP的starter：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

#### 2. 第二步：定义切面类
核心注解：`@Aspect`（标记这是一个切面类） + `@Component`（交给IOC容器管理）

```java
// 切面类：统一日志处理
@Aspect
@Component
public class LogAspect {
    // 这里定义切入点、通知
}
```

#### 3. 第三步：定义切入点（Pointcut）
用`@Pointcut`注解，配合切入点表达式，指定要切入哪些方法。

最常用的是`execution`表达式，语法：
```
execution(访问修饰符? 返回值类型 包名.类名.方法名(参数类型) 异常?)
```
- `?` 表示可选
- `*` 匹配任意字符
- `..` 匹配任意层级的包、任意数量的参数

##### 常用切入点示例：
```java
@Aspect
@Component
public class LogAspect {
    // 切入点1：切入controller包下所有类的所有方法
    @Pointcut("execution(* com.example.controller.*.*(..))")
    public void controllerPointcut() {}

    // 切入点2：切入service包下所有类的所有public方法
    @Pointcut("execution(public * com.example.service.*.*(..))")
    public void servicePointcut() {}

    // 切入点3：切入所有加了@RestController注解的类的方法
    @Pointcut("@within(org.springframework.web.bind.annotation.RestController)")
    public void restControllerPointcut() {}

    // 切入点4：切入所有加了@Transactional注解的方法
    @Pointcut("@annotation(org.springframework.transaction.annotation.Transactional)")
    public void transactionalPointcut() {}
}
```

#### 4. 第四步：定义通知（Advice）
Spring提供了5种通知类型，对应方法执行的不同时机：

| 通知类型 | 注解 | 执行时机 | 适用场景 |
|----------|------|----------|----------|
| 前置通知 | `@Before` | 目标方法执行之前 | 权限校验、参数校验 |
| 后置返回通知 | `@AfterReturning` | 目标方法正常执行返回之后 | 成功日志、数据返回处理 |
| 后置异常通知 | `@AfterThrowing` | 目标方法抛出异常之后 | 异常日志、告警 |
| 最终通知 | `@After` | 目标方法执行之后（无论正常还是异常，一定会执行） | 资源释放、清理操作 |
| 环绕通知 | `@Around` | 包围目标方法，在方法执行前后都可以执行逻辑，能控制方法是否执行 | 接口耗时统计、限流、事务、日志（最强大，能覆盖其他所有通知） |

##### 实战示例1：用@Around实现接口耗时统计（最常用）
```java
@Aspect
@Component
public class LogAspect {
    // 切入点：所有controller的方法
    @Pointcut("execution(* com.example.controller.*.*(..))")
    public void controllerPointcut() {}

    // 环绕通知
    @Around("controllerPointcut()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        // 1. 方法执行前：记录开始时间
        long start = System.currentTimeMillis();
        // 获取方法信息
        String methodName = joinPoint.getSignature().toShortString();
        Object[] args = joinPoint.getArgs();
        System.out.println("方法" + methodName + "开始执行，入参：" + Arrays.toString(args));

        Object result;
        try {
            // 2. 执行目标方法（必须写这行，不然目标方法不会执行）
            result = joinPoint.proceed();
            // 3. 方法正常返回后
            System.out.println("方法" + methodName + "执行成功，返回值：" + result);
        } catch (Throwable e) {
            // 4. 方法抛出异常时
            System.out.println("方法" + methodName + "执行失败，异常：" + e.getMessage());
            throw e; // 把异常抛出去，不影响原有业务
        } finally {
            // 5. 最终执行：计算耗时
            long end = System.currentTimeMillis();
            System.out.println("方法" + methodName + "执行耗时：" + (end - start) + "ms");
        }
        return result;
    }
}
```

##### 实战示例2：用@Before实现权限校验
```java
@Aspect
@Component
public class PermissionAspect {
    // 切入点：所有加了@NeedPermission注解的方法
    @Pointcut("@annotation(com.example.annotation.NeedPermission)")
    public void permissionPointcut() {}

    @Before("permissionPointcut()")
    public void before(JoinPoint joinPoint) {
        // 模拟权限校验
        if (!hasLogin()) {
            throw new RuntimeException("用户未登录，无权限访问");
        }
    }

    private boolean hasLogin() {
        // 实际开发中从Token、Session中获取用户信息
        return false;
    }
}
```

自定义注解`@NeedPermission`：
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface NeedPermission {
}
```

在接口上使用：
```java
@RestController
public class UserController {
    @NeedPermission // 加了这个注解，就会被权限切面切入
    @PostMapping("/add")
    public void addUser(User user) {
        // 只写核心业务代码，不用管权限校验
        userService.addUser(user);
    }
}
```

#### 5. 进阶：切面优先级@Order
如果有多个切面切入同一个方法，用`@Order`注解指定执行顺序，数字越小，优先级越高，越先执行：
```java
@Aspect
@Component
@Order(1) // 优先级最高，先执行
public class PermissionAspect {
}

@Aspect
@Component
@Order(2) // 后执行
public class LogAspect {
}
```

### 五、Spring AOP底层原理
Spring AOP的底层是**动态代理**，有两种实现方式，Spring会自动选择：
1.  **JDK动态代理**：基于接口实现，目标类必须实现接口，生成接口的代理实现类
2.  **CGLIB动态代理**：基于继承实现，目标类不需要实现接口，生成目标类的子类作为代理类

> Spring Boot 2.x之后，默认使用CGLIB动态代理，不管目标类有没有实现接口。

#### 关键区别：
| 特性 | JDK动态代理 | CGLIB动态代理 |
|------|-------------|---------------|
| 底层原理 | 实现目标类的接口 | 继承目标类 |
| 要求 | 目标类必须实现接口 | 目标类不能是final类，方法不能是final |
| 性能 | JDK1.8+之后性能优于CGLIB | 略低 |

### 六、开发中最常见的坑：AOP内部调用不生效
#### 1. 问题场景
```java
@Service
public class UserService {
    public void addUser() {
        System.out.println("添加用户");
        // 内部调用本类的方法
        this.updateUser();
    }

    @NeedPermission // 这个注解的AOP不生效！
    public void updateUser() {
        System.out.println("修改用户");
    }
}
```

当我们调用`addUser()`方法时，`updateUser()`上的AOP切面不会生效。

#### 2. 根本原因
AOP的本质是动态代理，只有调用**代理对象**的方法，才会走切面逻辑。
- 外部调用`addUser()`：调用的是代理对象的方法，会走切面
- 内部调用`this.updateUser()`：`this`是目标对象本身，不是代理对象，所以不会走切面

#### 3. 解决办法（3种，推荐第一种）
##### 方式1：把被调用的方法抽到另一个Bean里（推荐，符合设计规范）
```java
@Service
public class UserService {
    @Autowired
    private UpdateService updateService;

    public void addUser() {
        System.out.println("添加用户");
        // 调用其他Bean的方法，走代理
        updateService.updateUser();
    }
}

@Service
public class UpdateService {
    @NeedPermission
    public void updateUser() {
        System.out.println("修改用户");
    }
}
```

##### 方式2：从IOC容器里拿到代理对象，调用代理对象的方法
```java
@Service
public class UserService implements ApplicationContextAware {
    private ApplicationContext applicationContext;

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.applicationContext = applicationContext;
    }

    public void addUser() {
        System.out.println("添加用户");
        // 拿到代理对象
        UserService proxy = applicationContext.getBean(UserService.class);
        // 调用代理对象的方法，走切面
        proxy.updateUser();
    }

    @NeedPermission
    public void updateUser() {
        System.out.println("修改用户");
    }
}
```

##### 方式3：用`AopContext`获取当前代理对象
```java
@Service
public class UserService {
    public void addUser() {
        System.out.println("添加用户");
        // 拿到当前代理对象
        UserService proxy = (UserService) AopContext.currentProxy();
        // 调用代理对象的方法，走切面
        proxy.updateUser();
    }

    @NeedPermission
    public void updateUser() {
        System.out.println("修改用户");
    }
}
```
需要在启动类上开启暴露代理对象：
```java
@SpringBootApplication
@EnableAspectJAutoProxy(exposeProxy = true) // 开启暴露代理对象
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

---

## 第三部分：IOC & AOP的关系 & 面试高频题汇总
### 一、IOC和AOP的关系
1.  IOC是Spring的核心基石，AOP是Spring的核心功能，AOP依赖IOC容器实现
2.  IOC容器管理切面类（Aspect）的Bean，Spring启动时，IOC容器会为目标对象生成代理对象，把切面织入进去
3.  两者的核心目标都是**解耦**：IOC解决对象之间的耦合，AOP解决业务逻辑和横切逻辑的耦合

### 二、面试高频题汇总
1.  **什么是IOC？什么是DI？两者的关系？**
    答：IOC是控制反转，是一种设计思想，把对象的创建和管理的控制权交给容器；DI是依赖注入，是IOC思想的具体实现方式，容器自动把依赖的对象注入到需要的地方。

2.  **Spring Bean的生命周期？**
    答：容器启动→扫描类→实例化Bean→依赖注入→初始化方法（@PostConstruct）→Bean可用→容器关闭→销毁方法（@PreDestroy）。

3.  **Spring Bean的作用域有哪些？默认是哪个？**
    答：singleton（单例，默认）、prototype（多例）、request、session、application、websocket。

4.  **什么是AOP？核心应用场景？**
    答：AOP是面向切面编程，把横切逻辑抽离出来，不侵入业务代码实现功能增强；核心场景：日志、权限、事务、限流、异常处理。

5.  **Spring AOP的底层实现？JDK和CGLIB动态代理的区别？**
    答：底层是动态代理，有JDK动态代理（基于接口）和CGLIB动态代理（基于继承）两种实现；区别见上文表格。

6.  **AOP的通知类型有哪些？**
    答：前置通知@Before、后置返回通知@AfterReturning、后置异常通知@AfterThrowing、最终通知@After、环绕通知@Around。

7.  **同一个类内部方法调用，AOP为什么不生效？怎么解决？**
    答：因为AOP基于动态代理，内部调用用的是this目标对象，不是代理对象；解决办法见上文。

---

## 实战练习
1.  用Spring Boot搭建一个项目，用IOC实现Controller、Service、Dao的依赖注入
2.  用AOP实现一个全局日志切面，记录所有接口的入参、出参、耗时、异常
3.  用AOP实现一个自定义注解，实现接口限流功能
