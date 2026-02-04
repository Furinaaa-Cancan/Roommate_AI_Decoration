export const ROOM_TYPES = [
  {
    id: 'living_room',
    name: '客厅',
    nameEn: 'Living Room',
    icon: 'Sofa',
  },
  {
    id: 'bedroom',
    name: '卧室',
    nameEn: 'Bedroom',
    icon: 'Bed',
  },
  {
    id: 'dining_room',
    name: '餐厅',
    nameEn: 'Dining Room',
    icon: 'UtensilsCrossed',
  },
  {
    id: 'kitchen',
    name: '厨房',
    nameEn: 'Kitchen',
    icon: 'CookingPot',
  },
  {
    id: 'bathroom',
    name: '卫生间',
    nameEn: 'Bathroom',
    icon: 'Bath',
  },
  {
    id: 'study',
    name: '书房',
    nameEn: 'Study',
    icon: 'BookOpen',
  },
  {
    id: 'balcony',
    name: '阳台',
    nameEn: 'Balcony',
    icon: 'Sun',
  },
  {
    id: 'hallway',
    name: '玄关',
    nameEn: 'Hallway',
    icon: 'DoorOpen',
  },
] as const

export type RoomId = typeof ROOM_TYPES[number]['id']
