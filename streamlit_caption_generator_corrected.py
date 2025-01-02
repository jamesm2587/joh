import React, { useState } from 'react';
import { Calendar, Store, Type, DollarSign, Clock } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';

const emojiMapping = {
  "apple": "🍎", "banana": "🍌", "grape": "🍇", "mango": "🥭", "watermelon": "🍉",
  "orange": "🍊", "pear": "🍐", "peach": "🍑", "strawberry": "🍓", "cherry": "🍒",
  "kiwi": "🥝", "pineapple": "🍍", "blueberry": "🫐", "avocado": "🥑",
  "carrot": "🥕", "broccoli": "🥦", "corn": "🌽", "lettuce": "🥬", "tomato": "🍅",
  "potato": "🥔", "onion": "🧅", "garlic": "🧄", "pepper": "🌶️", "cucumber": "🥒",
  "mushroom": "🍄", "beef": "🥩", "chicken": "🍗", "pork": "🐖", "turkey": "🦃",
  "lamb": "🐑", "fish": "🐟", "shrimp": "🍤", "crab": "🦀", "lobster": "🦞",
  "salmon": "🐟", "tilapia": "🐟", "milk": "🥛", "cheese": "🧀", "butter": "🧈",
  "egg": "🥚", "yogurt": "🥄", "bread": "🍞", "rice": "🍚", "pasta": "🍝",
  "pizza": "🍕", "burger": "🍔", "taco": "🌮", "burrito": "🌯", "sushi": "🍣",
  "dessert": "🍰", "cake": "🎂", "cookie": "🍪", "ice cream": "🍦", "chocolate": "🍫"
};

const storeData = {
  "Ted's Fresh": {
    template: "{sale_type} ⏰\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
    location: "",
    hashtags: "#Meat #Produce #USDA #Halal #tedsfreshmarket #tedsmarket #grocerydeals #weeklydeals #freshproduce #halalmeats",
  },
  "IFM Market": {
    template: "{sale_type} ⏰\n{emoji} {item_name} {price}.\nOnly {date_range}\n.\n.\n{hashtags}",
    location: "",
    hashtags: "#Naperville #Fresh #Market #Produce #Meat #internationalfreshmarket",
  },
  "Fiesta Market": {
    template: "{emoji} {item_name} {price}.\n⏰ {date_range}\n➡️ {location}\n.\n.\n{hashtags}",
    location: "9710 Main St. Lamont, Ca.",
    hashtags: "#fiestamarket #grocerydeals #weeklyspecials #freshproduce #meats",
  },
  // ... add other stores
};

const CaptionGenerator = () => {
  const [formData, setFormData] = useState({
    store: "Ted's Fresh",
    itemName: "",
    priceFormat: "x lb",
    price: "",
    startDate: new Date().toISOString().split('T')[0],
    endDate: new Date(Date.now() + 6 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    saleType: "3 Day Sale"
  });
  const [caption, setCaption] = useState("");

  const getEmoji = (itemName) => {
    for (const [key, value] of Object.entries(emojiMapping)) {
      if (itemName.toLowerCase().includes(key)) {
        return value;
      }
    }
    return "🍽️";
  };

  const formatPrice = (price) => {
    const numPrice = parseFloat(price);
    if (isNaN(numPrice)) return "Invalid price";
    return Number.isInteger(numPrice) ? `${numPrice}¢` : `$${numPrice.toFixed(2)}`;
  };

  const generateCaption = () => {
    const store = storeData[formData.store];
    const emoji = getEmoji(formData.itemName);
    const formattedPrice = `${formatPrice(formData.price)} ${formData.priceFormat}`;
    const dateRange = `${new Date(formData.startDate).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' })} - ${new Date(formData.endDate).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' })}`;

    const caption = store.template
      .replace("{emoji}", emoji)
      .replace("{item_name}", formData.itemName)
      .replace("{price}", formattedPrice)
      .replace("{date_range}", dateRange)
      .replace("{location}", store.location)
      .replace("{hashtags}", store.hashtags)
      .replace("{sale_type}", formData.saleType);

    setCaption(caption);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <Card className="max-w-4xl mx-auto bg-white/80 backdrop-blur-lg shadow-xl">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center text-gray-800">
            Enhanced Caption Generator
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Store className="w-5 h-5 text-gray-500" />
                <select
                  className="w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500"
                  value={formData.store}
                  onChange={(e) => setFormData({ ...formData, store: e.target.value })}
                >
                  {Object.keys(storeData).map(store => (
                    <option key={store} value={store}>{store}</option>
                  ))}
                </select>
              </div>

              <div className="flex items-center space-x-2">
                <Type className="w-5 h-5 text-gray-500" />
                <Input
                  placeholder="Item Name"
                  value={formData.itemName}
                  onChange={(e) => setFormData({ ...formData, itemName: e.target.value })}
                  className="w-full"
                />
              </div>

              <div className="space-y-2">
                <Label className="text-sm font-medium">Price Format</Label>
                <RadioGroup
                  value={formData.priceFormat}
                  onValueChange={(value) => setFormData({ ...formData, priceFormat: value })}
                  className="flex space-x-4"
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="x lb" id="x-lb" />
                    <Label htmlFor="x-lb">x lb</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="x ea" id="x-ea" />
                    <Label htmlFor="x-ea">x ea</Label>
                  </div>
                </RadioGroup>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <DollarSign className="w-5 h-5 text-gray-500" />
                <Input
                  placeholder={`Price ${formData.priceFormat}`}
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  type="number"
                  step="0.01"
                  className="w-full"
                />
              </div>

              <div className="flex items-center space-x-2">
                <Calendar className="w-5 h-5 text-gray-500" />
                <Input
                  type="date"
                  value={formData.startDate}
                  onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
                  className="w-full"
                />
              </div>

              <div className="flex items-center space-x-2">
                <Clock className="w-5 h-5 text-gray-500" />
                <Input
                  type="date"
                  value={formData.endDate}
                  onChange={(e) => setFormData({ ...formData, endDate: e.target.value })}
                  className="w-full"
                />
              </div>

              {(formData.store === "Ted's Fresh" || formData.store === "IFM Market") && (
                <select
                  className="w-full p-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500"
                  value={formData.saleType}
                  onChange={(e) => setFormData({ ...formData, saleType: e.target.value })}
                >
                  <option value="3 Day Sale">3 Day Sale</option>
                  <option value="4 Day Sale">4 Day Sale</option>
                </select>
              )}
            </div>
          </div>

          <div className="mt-6">
            <Button 
              onClick={generateCaption}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-all duration-200 transform hover:scale-105"
            >
              Generate Caption
            </Button>
          </div>

          {caption && (
            <div className="mt-6">
              <Textarea
                value={caption}
                readOnly
                className="w-full h-48 p-4 bg-gray-50 rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CaptionGenerator;
