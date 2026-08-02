interface ShopProduct {
  id: number;
  name: string;
  price: number;
}

@Entry
@Component
struct Index {
  @State cartCount: number = 0;
  private products: ShopProduct[] = [
    { id: 1, name: 'AI 开发套件', price: 299 },
    { id: 2, name: '企业云沙箱', price: 599 }
  ];

  build() {
    Column({ space: 16 }) {
      Row() {
        Text('智造商城').fontSize(28).fontWeight(FontWeight.Bold)
        Blank()
        Text(`购物车 ${this.cartCount}`).fontColor('#0A59F7')
      }.width('100%')

      ForEach(this.products, (product: ShopProduct) => {
        Row({ space: 12 }) {
          Column({ space: 6 }) {
            Text(product.name).fontSize(18).fontWeight(FontWeight.Medium)
            Text(`¥${product.price}`).fontColor('#D73A49')
          }.alignItems(HorizontalAlign.Start)
          Blank()
          Button('加入购物车').onClick(() => this.cartCount += 1)
        }
        .padding(16)
        .borderRadius(12)
        .backgroundColor('#FFFFFF')
        .width('100%')
      }, (product: ShopProduct) => product.id.toString())
    }
    .padding(20)
    .backgroundColor('#F4F7FB')
    .width('100%')
    .height('100%')
  }
}

